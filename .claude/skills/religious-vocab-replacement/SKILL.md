---
name: religious-vocab-replacement
description: >
  将讲道稿、神学文章中的基督教宗教词汇批量替换为学术性或中性词汇，生成适合微信公众号发布的版本。

  【立即触发】以下任意情形均须调用本 skill，不得自行改写：
  - 用户说"洗稿"、"处理一下"、"公众号版本"、"发公众号"、"适合公众号"、"准备发公众号"
  - 用户提供文件路径 + 提到"公众号"或"微信"
  - 用户说"替换宗教词汇"、"词汇替换"、"发布前处理"
  - 用户提到内容审查、绕过审查、中性化处理讲道稿

  【不触发】用户只是要修改文章内容、补充论点、调整结构，而没有提到公众号/微信/洗稿。
---

# 宗教词汇替换

## 标准流程（直接调脚本）

给定源文件路径后，执行以下步骤：

**第一步：预览替换内容**

```bash
python "/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/.claude/skills/religious-vocab-replacement/scripts/replace_vocab.py" \
  "<源文件路径>" \
  --dry-run
```

**第二步：确认无误后正式写入**

```bash
python "/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/.claude/skills/religious-vocab-replacement/scripts/replace_vocab.py" \
  "<源文件路径>"
```

脚本会将洗稿版本直接写入 `302.公众号洗稿/<原文件名>`，**源文件保持不变**。

**第三步：输出替换统计**

将脚本打印的替换统计展示给用户。

---

## 算法说明

脚本使用两步替换：

1. **多字词**：按原词字数从长到短排列，顺序执行 `str.replace`。  
   例："神学"（2字）先于"神"（1字）处理 → "神学" → "关于至高者的学说"，之后"神"替换时文本中已无"神学"。

2. **单字"神"**：逐字扫描，检查前后字符，跳过"精神""神奇""神秘"等普通汉语词汇。

词汇表见 `references/vocab.json`，如需新增替换对，直接在 `vocab.json` 中添加 `["原词", "替换词"]` 条目即可（脚本读取时自动按长度降序排序）。

**输出路径注意**：脚本默认输出到 `302.公众号洗稿/<原文件名>`（根目录），需手动 `mv` 到对应子文件夹（如 `302.公众号洗稿/03.标杆人生/`）。
