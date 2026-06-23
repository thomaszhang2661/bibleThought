---
name: religious-vocab-replacement
description: 将文章中的基督教宗教词汇批量替换为学术性或中性词汇，适合在微信等审查平台发布。当用户说"洗稿"、"替换宗教词汇"、"发布前处理"、"词汇替换"，或给出文章路径要求处理时立即使用。
---

# 宗教词汇替换

## 标准流程（直接调脚本）

给定源文件路径后，执行以下步骤：

**第一步：运行替换脚本**

```bash
python "/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/.claude/skills/religious-vocab-replacement/scripts/replace_vocab.py" \
  "<源文件路径>" \
  --dry-run
```

先用 `--dry-run` 预览替换内容，确认无误后去掉 `--dry-run` 正式写入。

**第二步：复制到输出目录**

将处理后的文件复制到：
```
/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/302.公众号洗稿/
```

文件名保持原文件名。

**第三步：输出替换统计**

将脚本打印的替换统计展示给用户。

---

## 算法说明

脚本使用两步替换：

1. **多字词**：按原词字数从长到短排列，顺序执行 `str.replace`。  
   例："神学"（2字）先于"神"（1字）处理 → "神学" → "关于至高者的学说"，之后"神"替换时文本中已无"神学"。

2. **单字"神"**：逐字扫描，检查前后字符，跳过"精神""神奇""神秘"等普通汉语词汇。

词汇表见 `references/vocab-map.md`，如需新增替换对，在脚本 `REPLACEMENTS` 列表中添加即可（自动按长度排序）。
