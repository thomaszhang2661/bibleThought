# Flow Matching, Intuitively: A 15-Minute Talk Script

Paper: Lipman et al., *Flow Matching for Generative Modeling* (ICLR 2023)

> **The one sentence this whole talk is built around** Generating an image means pushing a noise point along a velocity field until it lands where real images live; flow matching trains that velocity field on randomly paired straight lines, and mean squared error automatically averages those lines into the right direction.

The script has four parts and follows the slides one to one (main slides 1–8 and 11–16; slides 9–10 are hidden and not shown; slides 17–19 are backup). **\[Show\]** marks which slide to put up. "Speaker note" blocks are extra explanation for us; they don't need to be read aloud.

---

## Part 1: An image is a point in space (about 3 minutes)

Almost everything that makes this paper hard comes down to one idea: **we need to think of an image as a single point in a very high-dimensional space.** Once that clicks, the rest follows.

**\[Show: slide 2\]**

In code, a 64×64 color image is a tensor of shape `(64, 64, 3)`. Flatten it and you get a vector of 12,288 numbers, each one the brightness of one color channel of one pixel. A vector of 12,288 numbers is a point in 12,288-dimensional space. So when I say "position" today, I don't mean where a pixel sits inside the picture. I mean where **the whole image** sits among all possible images. The color values themselves are the coordinates.

We can't draw 12,288 dimensions, so let's shrink the image as far as it goes: **a grayscale image with just 2 pixels.** Now an image is just 2 numbers, which is exactly a point in a plane.

**\[Show: slide 3, the two-pixel plane\]**

The horizontal axis is the brightness of pixel 1 and the vertical axis is the brightness of pixel 2. Move a point to the right and pixel 1 gets brighter; move it up and pixel 2 gets brighter. Every point in this plane is one complete two-pixel image.

Now look at where two kinds of points sit.

**Gray points are random noise images.** Each pixel is drawn independently from a standard Gaussian, so the two pixels have nothing to do with each other, and the gray points spread over the whole plane. At full size, that's what TV static looks like.

**Green points are "real images."** Real photos have structure: neighboring pixels usually have similar brightness. Sky sits next to sky, wall next to wall. So the two pixel values are close, and the points crowd into a narrow band along the diagonal.

Scale back up to 12,288 dimensions and the rule is exactly the same. Noise is a cloud that fills the whole space. Real photos occupy only a very thin, intricately shaped region, because pixels are full of structure: neighbors agree, there are edges, there are object shapes. Pick a random point in this space and you'll almost certainly get noise.

So in this space, "generate an image" becomes: **take any point from the noise cloud and move it into that thin region of real images.** Wherever it lands is the image you generate.

> Speaker note: Don't rush this part. You can ask the room, "What image is the point (0.9, −0.9)?" so people realize it's a picture that's bright on the left and dark on the right, and that it sits off the green band, so it doesn't look like a real image.

---

## Part 2: Generation means following a velocity field (about 1.5 minutes)

How do we move the point? Flow matching does it by learning a **velocity field**.

A velocity field is a function `v(x, t)`. You give it the current point x (an image) and the current time t, and it returns a vector the same shape as x that says "right now, from here, go in this direction at this speed." That function is the neural network we train. Architecturally it's usually a U-Net or a Transformer: an image goes in, and a same-sized "direction image" comes out.

The time t isn't real time. It's just a progress bar: t = 0 is pure noise and t = 1 is the finished image.

**\[Show: slide 4. The arrows are the velocity field at one moment; the colored curves are noise points following the arrows to real images.\]**

With a velocity field, generation is a very ordinary loop:

```python
x = torch.randn(64, 64, 3)      # start: a noise image
N = 20                          # number of steps
for k in range(N):
    t = k / N
    x = x + (1 / N) * v(x, t)   # take a small step along the arrow
# when the loop ends, x is the generated image
```

Mathematically this is solving an ordinary differential equation, an ODE.

What is an ODE? The unknown is a **function**, and the equation tells you how that function's derivative relates to the function itself; the function depends on just one variable, usually time t. The most familiar example is Newton's second law, where force determines acceleration:

**m · d²x/dt² = F(x)**

That has a second derivative, so it's a second-order ODE. Flow matching uses a first-order ODE, with only a first derivative:

**dx/dt = v(t, x)**

It says: where to go and how fast, at each moment, is decided by the current position and time. Written out in full, it's dx(t)/dt = v(t, x(t)) (the second equation in the top-left of slide 5): v is the known network, x(t) is the trajectory we're solving for, and wherever the particle is, it uses the velocity at that spot. The equation only says *how* to move; give it a starting point (the noise image) and the whole route is fixed.

The loop above is the simplest numerical method for this equation, called Euler's method: cut time into small pieces, assume the velocity is constant within each piece, and take a step. Every step calls the network once, so "how many steps" is the same as "how many network calls," and that directly sets how fast generation is.

Two properties are worth pointing out. First, the process is **deterministic**: the same noise always produces the same image. Second, **different starting points give different results**: every bit of variety in what the model generates comes from the random noise you start with.

So the whole problem reduces to one question: **how do we train this velocity field v?**

---

## Part 2 (continued): The physical picture (about 2.5 minutes)

This section takes a second, physics-flavored look at "generation means pushing a point along a velocity field." Slides 5 and 8 get the most time; slides 6 and 7 together take about a minute.

### Mian yu: transport, not creation

**\[Show: slide 5\]**

Start with the mian yu, "fish noodles," in the top right. You press a ball of dough through a colander and it comes out as lots of little noodles. That is exactly what flow matching does: the starting point is a shapeless lump (standard Gaussian noise), and a flow pushes and squeezes it until it splits into concentrated little pieces sitting where the data lives (the green ellipse on the left flowing into the green dots on the right). It doesn't paint an image from nothing; it **transports and redistributes** probability that's already there.

The flow tube in the middle is the math version of the same idea. A bundle of particles moves along the tube, and the number of particles (the probability) inside it is conserved from start to end: that's the continuity equation. Where the tube narrows, particles get packed more densely. The noise cloud starts as a wide Gaussian and gets squeezed all the way down onto the data, getting denser as it goes.

> Speaker note: the V₁ and V₂ labels on the tube come from incompressible flow, where a narrower tube means faster flow. Here what's conserved is probability, so a narrower cross-section means higher density, which you can write as p₁A₁ = p₂A₂. Mention this if someone asks.

### Unsteady flow, or steady flow?

Now the two pictures at the bottom. The velocity field v(t, x) depends explicitly on time: the same position has a different velocity at t = 0.2 and at t = 0.8. So **in x alone, this is an unsteady flow**, which is why the network has to take t as an input.

But treat time t as one more spatial direction and look in (t, x) space-time instead. There the field no longer changes with "time," and **every trajectory is a fixed streamline: it's a steady flow**. The trajectory plot in the bottom left, with t on the horizontal axis and x on the vertical, is exactly this space-time. Streamlines of a steady flow never cross, which is what we'll see on slide 13 as "averaged paths never cross."

### Three methods, three physical objects

**\[Show: slides 6 and 7\]**

These two slides put the three methods into one physical picture, with a slogan each to make them stick:

- **DDPM** starts from the **potential**. Maximum likelihood pushes down the potential −log p at the training images, but what the network actually fits is the **force field** at each time step.
- **Score matching** learns the **force** ∇log p directly: "which way is the data denser?"
- **Flow matching** talks about neither potential nor force. It learns the **velocity field that transports the density**.

The table on slide 7 sums it up: the three derivations start in different places, but for Gaussian paths what they end up learning can be converted into one another.

### Langevin dynamics: once you know the force, how do you sample?

**\[Show: slide 8\]**

If the score is a force, how do you turn it into samples? With Langevin dynamics. The picture is a double well with potential U(x) = −log p(x), so the valleys are where probability is high. A ball slides downhill under the force while being kicked around by random collisions.

With the force alone, the ball would roll into the nearest valley and stop there, giving you the same "most typical" point every time. With the random kicks, it jitters around the valley floor and now and then hops over the barrier into the other valley. Run it long enough, and the time it spends at each location follows the Boltzmann distribution p(x) ∝ e^{−U(x)}. That's sampling, not just finding the lowest point.

> Speaker note: diffusion models' stochastic sampling uses exactly this idea. Flow matching doesn't need the random kicks by default; particles just follow the deterministic velocity field. But you can add a Langevin term to it without changing the particle cloud at any moment (the result from MIT 6.S184 Lecture 3A). Bring this up only if asked.

That's the physical picture. Now back to the practical question: **how do we actually train this velocity field?**

---

## Part 3: How training works, and why it learns the right thing (about 4.5 minutes)

### The difficulty: there's no answer key

To train a regression network, you need input–answer pairs. Here the input is `(x, t)`, and the answer should be "the correct velocity at this point."

The problem is that nobody knows that answer. Nobody can tell you "this noise image should become that photo in the dataset," let alone which way to go at every point along the way.

### What the paper does: pair randomly, draw a straight line

**\[Show: slide 11\]**

Flow matching's approach is almost suspiciously simple:

```python
for step in range(num_steps):
    x1 = sample_from_dataset()     # a random real image
    x0 = torch.randn_like(x1)      # a random noise image (unrelated to x1)
    t  = torch.rand(1)             # a random time

    xt     = (1 - t) * x0 + t * x1 # the point on the line at time t: a blend of the two
    target = x1 - x0               # the velocity along this line: end minus start

    loss = ((v(xt, t) - target) ** 2).mean()
    loss.backward(); optimizer.step()
```

In words: grab a random real image and a random noise image, **pretend** that this noise is supposed to become this image, draw a straight line between them, and teach the network the velocity along that line.

Two things to notice. First, the noise and the image are drawn **independently**, so the pairing is completely arbitrary. This time a given noise is paired with a cat; next time the same noise might be paired with a car. Second, training **never solves an ODE**. Each step is one ordinary forward and backward pass, about as cheap as training an image classifier.

That second point is actually what the paper emphasizes most (the card at the bottom right of slide 11). Models that turn noise into data by following an ODE are called continuous normalizing flows, or CNFs, and they've existed since 2018. But training them used to require integrating the full ODE at every training step, which was too expensive to scale. Flow matching is the first method that turns CNF training into plain regression. So the paper's headline contribution is "scalable, simulation-free CNF training." Being able to generate high-quality images is a consequence of that breakthrough.

### The catch: the answers contradict each other

Because the pairing is random, many lines pass through the same point in space, and they head in different directions.

**\[Show: slide 12\]**

Here's the simplest possible example: one dimension, and a dataset with only two points, −2 and +2. Green lines go to +2; orange lines go to −2. You can see lots of them crossing.

Let's zoom in on one spot: time t = 0.5, position x = 0.5. Two kinds of lines pass through here. For a line heading to +2, the remaining distance is 1.5 and the remaining time is 0.5, so its velocity is **+3**. For a line heading to −2, the remaining distance is −2.5, so its velocity is **−5**.

So for the same input `(x = 0.5, t = 0.5)`, the training data sometimes says +3 and sometimes says −5. Which one should the network learn?

### The key: mean squared error averages them automatically

Anyone who has trained a regression model knows this fact: **if the same input appears with several different labels, the MSE-optimal prediction is the (weighted) average of those labels.** Squared loss E\[(v − y)²\] is minimized at v = E\[y\].

So how often does each label show up? That depends on how many lines heading to +2 and how many heading to −2 are crowded around x = 0.5 at t = 0.5.

At t = 0.5, the lines heading to +2 are exactly halfway there, so they're spread around +1. The lines heading to −2 are spread around −1. The point x = 0.5 is close to +1 and far from −1. If you count, about 98% of the lines passing here are heading to +2, and only 2% are heading to −2.

**\[Show: slide 13\]**

So what the network learns here is:

0.98 × (+3) + 0.02 × (−5) ≈ **+2.86**

Mostly toward +2, pulled back just a little by the other side.

> Speaker note: Where does 98% come from? At t = 0.5 both groups are Gaussians of width 0.5, centered at +1 and −1. The point x = 0.5 is one standard deviation from +1 and three standard deviations from −1. A Gaussian is about 55 times taller at one standard deviation than at three, so the ratio is roughly 55 : 1, which is 98% vs 2%. In the paper this is the "posterior weighting" in equation (8). If someone asks, you can explain it as "if you grab a particle at this spot, what are the odds it belongs to each group?"

### After averaging: one clean flow

The left side of slide 13 shows how particles actually move under the averaged velocity field the network learns. Compare it with slide 12: **the lines no longer cross.** Particles that start higher go to +2, particles that start lower go to −2, and they split cleanly.

That's not a coincidence. ODE trajectories can't cross, because one point can only have one velocity. Averaging takes a messy pile of random pairings and organizes it into an orderly transport plan.

Also notice the shape of the paths: flat at first, then splitting in the middle, then committing. Early on, the two groups overlap heavily, so of the lines passing any point, about half go up and half go down; they cancel out, the average velocity is near zero, and the particle "hesitates." As it moves along, which group it belongs to becomes clearer, and its velocity points more and more firmly to one side.

### Why the averaged flow is the right one

One more sentence on why this averaged field really does turn noise into real images.

Split the particles into groups by which data point they're heading to. Each group, moving along its own straight lines, clearly gets from noise to its target. Put all the groups together: the total flow at each point is the sum of the groups' flows, so the total velocity is the density-weighted average of the groups' velocities, which is exactly what the network learns. So when the averaged field pushes the whole noise cloud, the final distribution is the collection of all target points, which is the data distribution. In the paper this is Theorem 1.

The card at the bottom right of slide 13 is the paper's formal version of "averaging," Theorem 2. The paper defines two losses. L_FM is the one we actually want: fit the posterior-weighted average velocity, like the +2.86 we just computed. But that requires averaging over the entire dataset, so we can't compute it. L_CFM is the one we can compute: use a single line's velocity as the target each time, like +3 or −5. Theorem 2 proves these two losses differ only by a constant that doesn't depend on the network's parameters, so their gradients are identical and they train the same network. In other words, the intuition that "MSE averages automatically" is something the paper proves rigorously.

### Summary of this part

> **The questions are rough (randomly paired straight lines), but averaged over enough of them by MSE, the answer is exact.** We never need to know which noise should become which image; the network works out a sensible assignment on its own.

---

## Part 4: Compared with diffusion models (about 3 minutes)

### One minute on what diffusion models do

A diffusion model starts by defining a "noising process": take a real image and keep adding a bit of Gaussian noise until it becomes pure static. It's like a drop of ink spreading out in water, governed by fixed rules. Then the network is trained to **run that process backward**: given a noisy image, predict "what noise was mixed into it." To generate, you start from pure noise, predict the noise, remove a little, and repeat a few hundred times until you get a clean image.

### The training loop: almost identical, two lines apart

**\[Show: slide 14\]**

Put the two training loops side by side:

|  | Diffusion (DDPM) | Flow matching |
| --- | --- | --- |
| Sampling | a real image, a noise image, a time t | same |
| **How to mix** | a preset noise schedule: `sqrt(a_t) * x1 + sqrt(1 - a_t) * eps` | a straight line: `(1 - t) * x0 + t * x1` |
| **What the network predicts** | the noise that was added, `eps` | the velocity from noise toward the image, `x1 - x0` |
| Loss | mean squared error | same |
| At generation | a special sampler converts predicted noise into the next step | the predicted velocity goes straight into any ODE solver |

The training framework is almost the same: sample, mix, regress, MSE, and neither one simulates the generation process during training. They differ in only two lines: **how you mix**, and **what you predict**.

Those two lines boil down to one sentence:

**A diffusion model asks the network, "What noise is mixed into this image?" Flow matching asks, "Which way should I go from here?"**

The first gives you "what to remove," which you then have to convert into "where to go" with a formula. The second gives you the direction directly, and you just follow it. That's what the card on slide 14 means by "… then a sampler turns that into a step": both end up answering "where should I go," but diffusion answers an indirect question first and lets the sampler convert it.

### The real difference: they take different paths

The "how you mix" line decides the route particles take during training. Here's a one-dimensional example: start from noise x₀ = 1, end at data x₁ = 3, and see where each method is at different times.

**\[Show: slide 15\]**

| Time t | 0 | 0.2 | 0.5 | 0.8 | 0.9 | 1.0 |
| --- | --- | --- | --- | --- | --- | --- |
| Flow matching (straight line) | 1 | 1.4 | 2.0 | 2.6 | 2.8 | 3 |
| Diffusion (standard VP schedule) | 1 | 1.12 | 1.80 | 3.02 | **3.16** | 3 |

Flow matching moves in a straight line at constant speed. The diffusion path barely moves in the first half, then suddenly speeds up, **overshoots the target** at t = 0.9 (3.16 > 3), and finally comes back.

> Speaker note: If you want, you can also show screenshots of the paper's Figure 3 (diffusion trajectories overshoot, OT trajectories are straight) and Figure 6 (starting from the same noise, the diffusion model shows an image only at the very end).

### Why a straight path is better

At generation time, we walk this path step by step with a numerical method. On a straight path, you can take big steps without drifting off. On a curved path that speeds up and slows down, you have to take tiny steps around the bends, or you'll go off course.

The paper's experiments back this up. With the same network architecture and the same training budget, on CIFAR-10, flow matching needs about 140 network calls on average to generate an image, while the diffusion model (DDPM) needs about 270, and the image quality is better too. Flow matching also trains more stably and converges faster.

### An honest footnote

If someone asks "So aren't they basically the same thing?", the answer is: **to a large extent, yes.** For this family of Gaussian-blend paths, "predict the noise" and "predict the velocity" can be converted into each other mathematically; knowing one gives you the other. You can even plug the diffusion path directly into the flow matching framework and train it that way (the paper runs this experiment).

So the real difference is this: a diffusion model's route is **derived from** the rules of the noising process, so you don't get to choose it; flow matching lets you **design the route directly**, so you can pick the simplest one, a straight line.

The card in the middle of slide 15 is the paper's unified statement of this (Theorem 3). Every path the paper considers can be written as x_t = σ_t·x₀ + μ_t: each particle cloud has a center μ_t and a width σ_t, and particles move with the center and stretch with the width. The diffusion path and the straight-line path use the very same formula; they just change μ_t and σ_t over time in different ways. The straight path changes both at a constant rate. The diffusion path barely changes them in the first half and changes them sharply in the second half, which is exactly why it stalls and then overshoots. That's why the paper says diffusion models are a special case of the flow matching framework.

---

## Closing (about 0.5 minutes)

**\[Show: slide 16\]**

Back to the sentence we started with: **generating an image means pushing a noise point along a velocity field until it lands where real images live; flow matching trains that field on randomly paired straight lines, and mean squared error averages them into the right direction.** Compared with diffusion, the training framework is nearly identical, but the path is straighter, so generation is faster.

One last loose end: each training line is straight, but as we saw, the paths particles actually follow after averaging are curved. Straightening those paths is what later work like Rectified Flow sets out to do. And the guidance used for text-to-image generation, as well as generating in a compressed latent space, are covered in the later lectures of this course.

---

## Appendix: questions we might get

Slides 17 to 19 are backup slides. We don't show them in the main talk; we pull them up only if someone asks. The first four questions below map to those slides.

**Strictly speaking, what do Theorems 1 and 2 say?** (go to slide 17) Theorem 1 says the posterior-weighted average velocity field satisfies the continuity equation, so it really does carry the noise distribution to the data distribution. Theorem 2 says the loss trained on single-line velocities, L_CFM, has the same gradient as the loss trained on the average velocity, L_FM. The key step in the proof is expanding the square: in the cross term, taking the expectation of the conditional target gives exactly the marginal target, and what's left is a constant that doesn't depend on the parameters.

**How exactly is diffusion a special case?** (go to slide 18) For Gaussian paths, the velocity formula is "the center's velocity + the stretch rate × the distance from the center." Plug in the straight-line path's μ_t and σ_t and you get the constant velocity x₁ − x₀. Plug in the VP or VE diffusion μ_t and σ_t and you get a velocity field identical to diffusion's deterministic sampler (the probability flow ODE).

**How do you get 98%?** (go to slide 19) At t = 0.5 both groups are Gaussians of width 0.5, centered at +1 and −1. The point x = 0.5 is one standard deviation from +1 and three from −1, so the density ratio is e⁴ ≈ 55, which as probabilities is 98% vs 2%.

**What are the paper's limitations?** (go to slide 19) Each training line is straight, but the real trajectories after averaging are curved, and they aren't optimal transport in the global sense; the paper acknowledges this itself. Also, the experiments are mostly unconditional generation, which is still some distance from how text-to-image models are used today.

**Why not jump to the end in one step instead of taking many?** Because what the network learns at each point is the "average direction," and that average changes from place to place (that's why the trajectories we saw are curved). Jumping to the end in one step assumes the direction never changes, so you'd end up in the wrong place. The straighter the path, the fewer steps you can get away with, which is exactly why flow matching tries to make paths straight.

**Won't random pairing confuse the network?** No. Random pairing just makes each training label noisy, and MSE regression naturally averages out label noise. With enough training samples, the network learns the conditional expectation, which is the correct average velocity.

**Is there any correspondence between a noise image and a real image?** The only correspondence is "aligned by coordinate": the red channel of pixel (i, j) in the noise only blends with the red channel of pixel (i, j) in the image. Beyond that, the noise values at each coordinate have nothing to do with the image.

**Can flow matching compute the probability of an image?** Yes. Because it's an invertible ODE, you can integrate an image backward to the noise end and compute its exact likelihood, which is an extra advantage over ordinary diffusion models (paper, Appendix C). But today's focus is generation, so we're skipping that.