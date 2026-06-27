#!/usr/bin/env python3
"""
批量替换中文神学文章中的宗教词汇。
替换规则从 references/vocab.json 读取，按原词字数从多到少排序。
单字"神"特殊处理：负向字符集扫描，跳过"精神""神奇"等普通词。

用法：
  python replace_vocab.py <文件或目录> [--dry-run]
"""

import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VOCAB_FILE = SCRIPT_DIR.parent / "references" / "vocab.json"

# 从 vocab.json 加载，按原词字数降序排列（长词先替换，避免短词破坏长词）
REPLACEMENTS = sorted(json.loads(VOCAB_FILE.read_text(encoding="utf-8")), key=lambda x: -len(x[0]))

# "神" 单字替换：出现在这些字之后或之前时跳过
# 例：精神、心神、神经、神奇、神秘、神圣、神话、神情、神明
SHEN_PREV_SKIP = set("精心凡鬼诸仙")
SHEN_NEXT_SKIP = set("学经话奇秘情色明龛志士格言仙圣")


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


OUTPUT_DIR = Path("/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/302.公众号洗稿")


def process_file(path: Path, dry_run: bool, output_dir: Path):
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
        out_path = output_dir / path.name
        out_path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path.name}：")
        for c in changes:
            print(c)
        print(f"  → 已写入 {out_path}")


def main():
    parser = argparse.ArgumentParser(description="宗教词汇批量替换")
    parser.add_argument("target", help="文件路径或目录")
    parser.add_argument("--dry-run", action="store_true", help="预览，不修改文件")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="输出目录（默认：302.公众号洗稿）")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not args.dry_run:
        output_dir.mkdir(parents=True, exist_ok=True)

    target = Path(args.target)
    if target.is_file():
        process_file(target, args.dry_run, output_dir)
    elif target.is_dir():
        # 目录模式：在输出目录下建同名子文件夹，保留相对路径结构
        dir_output = output_dir / target.name
        files = sorted(target.rglob("*.md"))
        print(f"找到 {len(files)} 个 .md 文件，输出至 {dir_output}\n")
        for f in files:
            rel = f.relative_to(target)
            dest_dir = dir_output / rel.parent
            if not args.dry_run:
                dest_dir.mkdir(parents=True, exist_ok=True)
            process_file(f, args.dry_run, dest_dir)
    else:
        print(f"错误：找不到 {target}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
