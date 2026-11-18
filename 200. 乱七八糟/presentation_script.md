# 1

Hi everyone, I’m Taha, and with Jian and Bohan we’re working on making the KV cache of large language models smaller and faster on NVIDIA’s Hopper GPUs, the H100 and H200. We’ll show why existing 4-bit kernels are actually slower than 8-bit ones on these GPUs, what we built to fix it, and what it costs in accuracy.

# 2 Why this project?

Three reasons. First, the trend: 4-bit is where the field is going. NVIDIA’s newest GPUs run NVFP4 natively, and a 4-bit KV cache takes about half the memory of FP8, so you get longer contexts and more users per GPU.

Second, the installed base: most GPUs serving models today are Hopper, the H100 and H200. They support FP8 in hardware, but not FP4.

Third, the gap: vLLM can already store an NVFP4 KV cache on Hopper, but it decodes it in software, and attention ends up slower than plain BF16.

 <!-- Hopper has no FP4 hardware, so every 4-bit value has to be converted in software before the tensor cores can use it, and that makes attention slower than plain BF16. -->

So if we can make 4-bit pay off on the GPUs that are already deployed, every one of them can serve longer contexts and more users, with no new hardware.

<!-- Hopper is the largest installed base for inference today, and these GPUs will keep serving for years. Saving memory and time on them is real money. -->

# 3 Decoding is limited by reading the KV cache

Here’s the key fact about decoding. To generate each token, the model reads the entire KV cache. Take one row of K: 128 numbers in BF16, that’s 256 bytes. The four query heads that share it do about a thousand operations on it, so only about 4 operations per byte.

But an H200 can do about 200 operations for every byte it reads. So the compute units mostly sit waiting for memory, and the time is roughly bytes divided by bandwidth.

That’s why a smaller KV cache matters: storing it in 4 bits, one row takes 72 bytes instead of 256 in BF16, and about half of FP8’s 128

# 4 The surprise: 4-bit is slower than FP8 on Hopper

Here is the surprise. This is a kernel benchmark of one attention layer, with Llama-3.1-8B’s shape, 32 sequences of 16K tokens. On an H200, FlashInfer, the attention library behind vLLM, takes half a millisecond in BF16 and 0.4 in FP8.

NVFP4 reads only 28 percent of BF16’s bytes, so it should be the fastest. Instead it takes 0.67 milliseconds: slower than BF16, and about 1.7 times slower than FP8. It uses only 19 percent of the memory bandwidth.

And this is exactly the kernel a vLLM user gets today with an NVFP4 KV cache on Hopper. So the question became: why?

<!-- Llama3.1-8B is the most common benchmark model for LLM inference, and its attention shape, 8 KV heads with 4 query heads each and head dimension 128, is shared by many current models. The kernel’s speed depends only on that shape, so the results carry over. -->

<!-- TensorRT-LLM is NVIDIA’s own inference library. We compared against what vLLM uses; TensorRT-LLM’s FP8 decode kernel is the next baseline we plan to add. -->

# 5 Why: too many instructions, and too much waiting

So why are they slow? We counted the instructions each kernel actually executes, using a tool called NVBit.

The key number is on the right: the issue budget. An H200 can issue about 33 trillion thread-instructions per second and read 4.8 terabytes per second, so to keep memory busy, a kernel can afford only about 7 instructions per byte.

Now look at the table. Our first Triton kernel needed about 21 instructions per byte, and FlashInfer about 15: two to three times over budget. That’s the first problem: too many instructions.

BitDecoding, a research kernel built specifically for low-bit KV decoding, is interesting: it stays within the budget, at 6.7, yet it still reaches only about 25 percent of bandwidth. That’s the second problem: waiting. Loading, decoding and the matrix multiply run one after another, so either the memory or the compute sits idle.

So a fast kernel needs both: few instructions per byte, and overlap of loading, decoding and compute.

<!-- BitDecoding use INT4, we are comparing NVFP4, not exactly match. BitDecoding is the strongest research kernel we found for 4-bit KV on Hopper. We used it to diagnose why kernels are slow, not as a head-to-head speed comparison; our own INT4 kernel is also faster than FOSCAR’s INT4 kernel at the same bytes. -->

# 6 Our design: a Hopper-native CUDA kernel

Our kernel answers those two problems directly.

On the left, the waiting. A GPU has a large but slow main memory, and each of its compute units has a small, fast on-chip memory called shared memory，which is shared by the warps on the compute unit. In our kernel, one warp, only copies 4-bit data from main memory into shared memory, using Hopper’s copy engine, TMA. Two other groups of warp take turns: while one decodes and multiplies a tile on the tensor cores, the other works on the next. The KV cache is read in tiles of 256 tokens, so in the timeline, blue is loading a tile and orange is computing it, and they overlap.

On the right, too many instructions. Three changes. First, we store K and V in the order the tensor cores read them, so decoded values go straight from registers into the tensor cores, with no round trip through shared memory. Second, we swap the matrix operands: the four query heads fill 8 columns instead of being padded to 64 rows, so softmax stops working on empty rows. Third, we decode with bit tricks: mask instead of shift, build floats directly from bit patterns, and apply each scale once per group.

Together, instructions per value drop from about 12 to about 2 for INT4 and 3.8 for NVFP4, back near the budget.

<!-- We put K first, so each tensor-core instruction covers 64 tokens, and the four query heads only need padding to 8 columns instead of 64 rows. -->

# 7 Result: 4-bit now beats FP8

Here are the results. First, the kernel alone, one attention layer, on the same benchmark as before: our NVFP4 kernel takes 0.19 milliseconds, against 0.40 for FlashInfer’s FP8 and 0.67 for its NVFP4. Across 11 shapes, it’s 1.4 to 2.3 times faster than FP8, and it reaches about 70 to 76 percent of memory bandwidth, up from 19.

Most importantly, this carries over to real serving. End to end, for the whole model inside vLLM, with the full accuracy recipe, decoding is 1.12 to 1.64 times faster than the fastest FP8 path at batch 8 and above, level at batch 1, and 1.63 times as many requests fit in memory. The end-to-end gain is smaller than the kernel gain because each step also reads the model weights.

And under load it matters even more. Serving a reasoning-like stream, 1K tokens in and 8K out, 99 percent of our requests still met their latency targets at 1.25 requests per second. FP8 already fell short at 1.0: its cache filled up, requests were preempted, and the slowest ones waited over two minutes for their first token. That’s the practical value: more users per GPU.

 <!-- FP8  at 1 req/sec 96.5 percent, just under the 99 percent bar, but the tail was very bad: the slowest requests waited 135 seconds for their first token. -->

<!-- one run per rate so far -->

# 8 Accuracy: a recipe that passes on three models

Speed is only useful if accuracy holds. Our recipe is NVFP4, plus two cheap fixes for K, removing its mean and rotating it, and keeping the first four tokens in BF16.

The table shows why the mean removal matters. Rotation alone works on Llama and Mistral, but on Qwen3 it breaks: perplexity jumps by 1.38. That’s because Qwen3’s keys carry a large shared offset, and rotation spreads it into every group. Removing the mean first fixes it, and all three models stay within our bound.

On the right, a surprise about FP8 itself. On a reasoning model, R1-Distill-Qwen-7B, FP8 drops math accuracy from 73.5 to 0.5 percent. We traced it to layer 0, and keeping just that one layer in BF16 restores it, for FP8 and for our 4-bit recipe.

Inside vLLM, on all 500 MATH problems with five runs each, our recipe shows no significant difference from BF16 on two models, and perplexity rises only 0.06 percent, against 0.94 for FP8.

<!-- We follow StreamingLLM, which found four initial tokens are enough across models. Keeping four costs almost nothing compared with thousands of tokens, and protecting the sink matters: without it, our error on Llama is about 25 percent worse. We haven’t compared one versus four directly; that’s an easy ablation to add. -->

<!--
SageAttention is an 8-bit attention method from Tsinghua; we borrow its “smooth K” trick, subtracting K’s mean. FlagRot, from HKUST, showed that rotating keys can hurt on some models like Qwen3; we fix that by removing the mean before rotating. -->

# 9 Impact on real serving

Beyond the numbers, this already works in a real system. Our plugin runs the full recipe inside vLLM: faster than its fastest FP8 path, with 1.63 times the capacity and no significant accuracy loss.

We’ve also started contributing back to vLLM. We posted our analysis of why FP8 silently breaks Qwen2-family models at layer 0. We gave a minimal reproducer for a prefix-cache bug that makes two 4-bit formats give wrong answers; that bug now has a fix, and we contributed the test it was missing. And we filed an issue showing that one constant in vLLM’s own 4-bit format, UltraQuant, can be tuned to cut its error by 40 to 56 percent at the same size.

Our goal is a Hopper path for 4-bit KV in vLLM itself, and then NVFP4 in FlashInfer.

中文意思：

除了这些数字，这套方法已经在真实的系统里跑起来了。我们的插件在 vLLM 里运行完整的配方：比 vLLM 里最快的 FP8 路径还快，能放下的请求是 FP8 的 1.63 倍，而且精度没有明显的损失。

我们也已经开始回馈 vLLM 社区。我们发布了对 FP8 为什么会在 Qwen2 系列模型的第 0 层“悄悄出错”的分析；提供了一个最小的复现程序，复现一个会让两种 4 位格式给出错误答案的前缀缓存 bug，现在这个 bug 已经有人提交了修复，我们补上了它缺少的测试；我们还提交了一个 issue，指出 vLLM 自带的 4 位格式 UltraQuant 里有一个常数，调整之后在同样的存储大小下，误差可以降低 40% 到 56%。

我们的目标是在 vLLM 本身里加入一条 Hopper 上的 4 位 KV 路径，然后再把 NVFP4 的支持加进 FlashInfer。

# 10 Question, status, and plan to December

To wrap up. Our question was: on Hopper, which has no FP4 tensor cores, can a 4-bit KV cache decode faster than FP8 while staying within about one point of BF16 accuracy?

In short, the kernel is up to 2.3 times faster than FP8, it carries over to vLLM and to serving under load, and accuracy holds.

Our plan to the poster on December 16: Taha will repeat the serving runs and add shared-prefix workloads; we’ll run long reasoning at 8K to 16K tokens and more models; then freeze the results and publish the code with a one-command reproduction.

And what’s still open, honestly: time to first token is 1.5 to 6 percent slower; at batch 1 we’re level with FP8, not faster; the static K mean may not hold for very long generations; and the kernel is Hopper only.

So far, the answer is yes: about 0.6 times FP8’s bytes, faster than the fastest FP8 path, with no significant accuracy loss. Thank you, we’re happy to take questions.

12 月 2 日：服务测试多跑几次，并加上共享前缀的负载（Taha 负责）
现在的服务测试每个请求速率只跑了一次，要多跑几次，给出结果的波动范围；再加一种“很多请求共用一段很长的开头”的负载，比如多轮对话、agent 反复使用同一段系统提示。
12 月 9 日：长推理（8K–16K 个 token）和更多模型
测试模型生成很长的推理过程时，精度是否还能保持。这是目前最大的隐患：静态的 K 均值是用较短的文本标定的，生成很长时可能不再准确。同时在更多的模型上验证。
12 月 12 日：冻结结果，整理好代码仓库，做到一条命令就能复现
不再加新的实验，所有数字定下来；把代码仓库整理干净，README 里写清楚怎样安装、用哪一条命令复现论文的主要结果（这正好对应评分标准里代码那 20 分）。
12 月 16 日：海报展示 · 12 月 18 日：提交书面报告
课程的两个截止日期。
