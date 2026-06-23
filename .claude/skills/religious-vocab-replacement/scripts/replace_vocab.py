#!/usr/bin/env python3
"""
批量替换中文神学文章中的宗教词汇。
替换规则：按原词字数从多到少排序，避免短词先替换导致长词被拆散。
单字"神"特殊处理：负向字符集扫描，跳过"精神""神奇"等普通词。

用法：
  python replace_vocab.py <文件或目录> [--dry-run]
"""

import sys
import argparse
from pathlib import Path

# 所有替换对：按原词字数从长到短排列（代码自动排序，此处仅供人工阅读）
# 关键：长词先替换，"神学" → "关于至高者的学说" 之后，"神" 替换时就不会破坏它
REPLACEMENTS = [
    ("耶稣基督",    "伊诶溯斯受膏者"),
    ("基督徒",      "受膏者的跟随者"),
    ("基督教",      "受膏者信仰"),
    ("神学思想",    "关于至高者的思想"),
    ("神学观点",    "关于至高者的观点"),
    ("神学家",      "圣学学者"),
    ("神学院",      "圣学院"),
    ("神学",        "关于至高者的学说"),
    ("传福音",      "分享好消息"),
    ("耶稣",        "伊诶溯斯"),
    ("基督",        "受膏者"),
    ("上帝",        "至高者"),
    ("教会",        "会众"),
    ("圣经",        "圣典"),
    ("福音",        "好消息"),
    ("圣灵",        "神圣之灵"),
    ("受洗",        "受洁净之礼"),
    ("洗礼",        "洁净之礼"),
    ("牧师",        "小牧人"),
    ("天国",        "至高者的国度"),
    ("天堂",        "至高者的国度"),
    ("祷告",        "祈求"),
    ("救主",        "拯救者"),
    ("救恩",        "拯救"),
    ("罪人",        "冒犯者"),
    ("罪恶",        "恶行"),
    ("罪孽",        "过犯"),
]

# 按原词字数降序排列（确保无论用户如何修改上面列表，顺序始终正确）
REPLACEMENTS = sorted(REPLACEMENTS, key=lambda x: -len(x[0]))

# "神" 单字替换：出现在这些字之后或之前时跳过
# 例：精神、心神、神经、神奇、神秘、神圣、神话、神情、神明
SHEN_PREV_SKIP = set("精心凡鬼诸仙")
SHEN_NEXT_SKIP = set("学经话奇秘情色明龛志士格言仙")


def replace_shen(text: str) -> tuple[str, int]:
    """单字"神"的安全替换，返回 (新文本, 替换次数)。"""
    result = []
    count = 0
    for i, ch in enumerate(text):
        if ch == "神":
            prev = text[i - 1] if i > 0 else ""
            nxt  = text[i + 1] if i < len(text) - 1 else ""
            if prev in SHEN_PREV_SKIP or nxt in SHEN_NEXT_SKIP:
                result.append("神")
            else:
                result.append("至高者")
                count += 1
        else:
            result.append(ch)
    return "".join(result), count


def process_text(text: str) -> tuple[str, list[str]]:
    changes = []

    # 第一步：多字词，从长到短批量替换
    for original, replacement in REPLACEMENTS:
        count = text.count(original)
        if count:
            text = text.replace(original, replacement)
            changes.append(f"  {original} → {replacement}（{count}处）")

    # 第二步：单字"神"，负向字符集扫描
    text, shen_count = replace_shen(text)
    if shen_count:
        changes.append(f"  神 → 至高者（{shen_count}处）")

    return text, changes


def process_file(path: Path, dry_run: bool):
    content = path.read_text(encoding="utf-8")
    new_content, changes = process_text(content)

    if not changes:
        print(f"⏭  {path.name} — 无需替换")
        return

    if dry_run:
        print(f"🔍 {path.name}（预览）：")
        for c in changes:
            print(c)
    else:
        path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path.name}：")
        for c in changes:
            print(c)


def main():
    parser = argparse.ArgumentParser(description="宗教词汇批量替换")
    parser.add_argument("target", help="文件路径或目录")
    parser.add_argument("--dry-run", action="store_true", help="预览，不修改文件")
    args = parser.parse_args()

    target = Path(args.target)
    if target.is_file():
        process_file(target, args.dry_run)
    elif target.is_dir():
        files = sorted(target.rglob("*.md"))
        print(f"找到 {len(files)} 个 .md 文件\n")
        for f in files:
            process_file(f, args.dry_run)
    else:
        print(f"错误：找不到 {target}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
