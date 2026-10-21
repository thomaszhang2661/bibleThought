---
name: md-to-docx
description: >
  将本仓库中的 Markdown 笔记（.md）转换为排版过的 Word 文档（.docx），
  用于导出、打印、投稿或分享给不用 Markdown 的人。

  【触发】用户说"给我 word 版"、"导出成 word"、"转成 docx"、"生成 Word 文档"，
  并且指明了具体的 .md 文件，或一个文件夹/分类（"这一篇"、"这一套"、
  "这个文件夹下的全部"）。

  【不触发】用户只是要新建、编辑或翻译 markdown 内容本身，没有提到要 word/docx 格式。
---

# Markdown → Word 转换

本仓库自带一个 Node 脚本（`scripts/md2docx.js`），把 Markdown 转换成排版过的
.docx：标题样式、加粗/斜体、项目符号与编号列表（含嵌套）、表格、脚注
（`[^x]` + `[^x]: 说明`）、分隔线 `---`、超链接。它不依赖系统安装 pandoc
（这台机器上 Homebrew 版 pandoc 需要从源码编译，非常慢），只依赖 `docx` 和
`markdown-it` 两个小型 npm 包。

## 使用步骤

1. **确认依赖已安装**（第一次用，或 `node_modules` 被 git 忽略掉之后）：
   ```bash
   cd "<repo_root>/.claude/skills/md-to-docx"
   [ -d node_modules ] || npm install
   ```

2. **转换单个文件**，输出路径一般与输入同目录、同名、后缀改为 `.docx`：
   ```bash
   node "<repo_root>/.claude/skills/md-to-docx/scripts/md2docx.js" \
     "<输入.md的绝对路径>" "<输出.docx的绝对路径>"
   ```

3. **批量转换一个文件夹（含子文件夹）**：
   ```bash
   SKILL_DIR="<repo_root>/.claude/skills/md-to-docx"
   find "<目标文件夹>" -name "*.md" | while IFS= read -r f; do
     node "$SKILL_DIR/scripts/md2docx.js" "$f" "${f%.md}.docx"
   done
   ```

4. **校验生成的文件**（推荐，用 `docx` skill 自带的校验器）：
   ```bash
   python3.11 ~/.claude/skills/docx/scripts/office/validate.py "<输出.docx>"
   ```
   若系统默认 `python3` 版本低于 3.10（报 `match` 语句的 `SyntaxError`），
   改用 `python3.11` 或 `python3.12`（`which -a python3.11 python3.12` 确认可用）。

## 转换规则

- `#` ~ `####` → Word 标题样式 1–4（黑体加粗）
- `**粗体**` / `*斜体*` → 对应加粗/斜体
- 无序/有序列表（含嵌套）→ Word 原生项目符号/编号列表，不是 Unicode `•`
- 表格 `| a | b |` → Word 表格，首行浅色底纹
- 脚注 `[^label]` + 对应的 `[^label]: 说明文字` → 转换为 Word 真正的脚注
  （页面底部自动编号），而不是把方括号原样留在正文里
- `---` 分隔线 → 一条水平分隔线
- 链接 `[文字](url)` → 可点击超链接
- 正文默认字体宋体（SimSun）、标题黑体（SimHei），纸张 US Letter；
  如需换字体/纸张，改 `scripts/md2docx.js` 里 `bodySize` 附近与 `page.size` 的常量

## 已知局限

- 不处理内嵌图片（本仓库笔记目前基本不用图片）
- 行内 HTML 会被忽略，不会报错也不会渲染
- 删除线 `~~text~~` 不转换（markdown-it 默认不解析；如需要可加
  `markdown-it` 的 strikethrough 相关插件并在脚本里注册）
- 多文件批量转换时，文件名以数字开头的会在文档标题里去掉编号前缀
  （例如 `01.如何理解三位一体.md` → 标题显示为"如何理解三位一体"），
  如不需要这个行为，删掉脚本里 `titleBase.replace(...)` 那一行
