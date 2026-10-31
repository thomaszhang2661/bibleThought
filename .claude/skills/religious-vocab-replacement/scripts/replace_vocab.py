#!/usr/bin/env python3
"""
批量替换中文神学文章中的宗教词汇。
替换规则从 references/vocab.json 读取，按原词字数从多到少排序。
单字"神"特殊处理：负向字符集扫描，跳过"精神""神奇"等普通词。

用法：
  python replace_vocab.py <文件或目录> [--dry-run]      # 替换并写入，写入后自动做合规扫描
  python replace_vocab.py <文件或目录> --audit-only      # 只扫描，不替换

合规扫描规则在 references/audit-rules.json，“神”的保护词在 references/shen-protected.json，
发现新的误伤词或残留类型时直接往这两个文件里补。
"""

import re
import sys
import json
import argparse
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
VOCAB_FILE = SCRIPT_DIR.parent / "references" / "vocab.json"

# 从 vocab.json 加载，按原词字数降序排列（长词先替换，避免短词破坏长词）
REPLACEMENTS = sorted(json.loads(VOCAB_FILE.read_text(encoding="utf-8")), key=lambda x: -len(x[0]))

SHEN_PROTECTED = json.loads((SCRIPT_DIR.parent / "references" / "shen-protected.json").read_text(encoding="utf-8"))
AUDIT_RULES = json.loads((SCRIPT_DIR.parent / "references" / "audit-rules.json").read_text(encoding="utf-8"))

# "神" 单字替换：出现在这些字之后或之前时跳过
# 例：精神、心神、神经、神奇、神秘、神圣、神话、神情、神明
SHEN_PREV_SKIP = set("精心凡鬼诸仙")
SHEN_NEXT_SKIP = set("学经话奇秘情色明龛志士格言仙圣")


def is_protected(text: str, i: int) -> bool:
    """text[i] 的“神”是否落在 shen-protected.json 的某个保护词内。"""
    for word in SHEN_PROTECTED:
        k = word.find("神")
        while k != -1:
            start = i - k
            if start >= 0 and text[start:start + len(word)] == word:
                return True
            k = word.find("神", k + 1)
    return False


def replace_shen(text: str) -> tuple[str, int]:
    """单字"神"的安全替换，返回 (新文本, 替换次数)。"""
    result = []
    count = 0
    for i, ch in enumerate(text):
        if ch == "神":
            prev = text[i - 1] if i > 0 else ""
            nxt  = text[i + 1] if i < len(text) - 1 else ""
            if prev in SHEN_PREV_SKIP or nxt in SHEN_NEXT_SKIP or is_protected(text, i):
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


VARIANTS = ["关于至高者的学说", "圣学院", "圣学学者"]


def residual_rule() -> dict:
    """由 vocab.json 自动生成“残留”规则：词表里的原词若还留在输出里，就是没替换到。
    词表一更新，扫描自动跟着更新；原词若出现在任何替换词里则跳过，避免自我误报。"""
    replacements = "".join(b for _, b in REPLACEMENTS)
    keys = [a for a, _ in REPLACEMENTS if a not in replacements]
    return {
        "id": "residual-term", "category": "三、替换体例（残留）", "clause": "3.1", "confirm": True,
        "regex": "|".join(re.escape(k) for k in keys),
        "note": "词表里的原词仍在文中；书名、引语、文献出处（3.3）可保留，其余询问作者统一写法",
    }


def audit_text(text: str) -> list[tuple[str, str, str]]:
    """按 audit-rules.json 扫描，返回 [(类别·条款, 提示, 片段)]。只报告，不修改。
    同一规则下相同的词每篇只报一条（带次数和首见行号），避免长文刷屏。"""
    findings = []
    lines = text.splitlines()
    for rule in AUDIT_RULES + [residual_rule()]:
        pattern = re.compile(rule["regex"])
        label = f'{rule["category"]}（{rule["clause"]}）' + ("【需作者确认】" if rule.get("confirm") else "")
        allow = set(rule.get("allow", []))
        seen = {}  # token -> [count, first_line_no, context]
        for n, line in enumerate(lines, 1):
            if rule.get("headings_only") and not line.startswith("#"):
                continue
            if rule["id"] in ("evade-acronym", "english-mixed"):
                line = re.sub(r"https?://\S+", "", line)  # 先去掉 URL，避免把 %E8%AF 当缩写
            if rule.get("min_cjk") and len(re.findall(r"[\u4e00-\u9fff]", line)) < rule["min_cjk"]:
                continue
            for m in pattern.finditer(line):
                tok = m.group()
                if tok in allow or (rule.get("skip_roman") and re.fullmatch(r"[IVXLCDM]+", tok)):
                    continue
                if tok in seen:
                    seen[tok][0] += 1
                else:
                    a, b = max(0, m.start() - 8), min(len(line), m.end() + 8)
                    seen[tok] = [1, n, line[a:b]]
        for tok, (cnt, n, ctx) in seen.items():
            times = f"×{cnt} " if cnt > 1 else ""
            findings.append((label, rule["note"], f"「{tok}」{times}首见L{n}…{ctx}…"))
    present = [v for v in VARIANTS if v in text]
    if len(present) > 1:
        findings.append(("三、替换体例（一致性）（3.1）【需作者确认】", "同篇多种写法并存，询问作者统一", "、".join(present)))
    return findings


def print_audit(name: str, text: str):
    findings = audit_text(text)
    if not findings:
        print(f"  🟢 合规扫描：{name} 未发现机器可查的风险（政治/影射/事实核对仍需按 references/compliance-checklist.md 人工审校）")
        return
    print(f"  🟡 合规扫描：{name} 共 {len(findings)} 处，按类别：")
    last = None
    for label, note, where in findings:
        if label != last:
            print(f"    ▶ {label}｜{note}")
            last = label
        print(f"       {where}")


OUTPUT_DIR = Path("/Users/zhangjian/Library/Mobile Documents/iCloud~md~obsidian/Documents/BibleThought/302.公众号洗稿")


def process_file(path: Path, dry_run: bool, output_dir: Path, audit_only: bool = False):
    content = path.read_text(encoding="utf-8")
    if audit_only:
        print(f"🔎 {path.name}")
        print_audit(path.name, content)
        return
    new_content, changes = process_text(content)

    if not changes:
        print(f"⏭  {path.name} — 无需替换")
        print_audit(path.name, content)
        return

    if dry_run:
        print(f"🔍 {path.name}（预览）：")
        for c in changes:
            print(c)
        print_audit(path.name, new_content)
    else:
        out_path = output_dir / path.name
        out_path.write_text(new_content, encoding="utf-8")
        print(f"✅ {path.name}：")
        for c in changes:
            print(c)
        print(f"  → 已写入 {out_path}")
        print_audit(path.name, new_content)


def main():
    parser = argparse.ArgumentParser(description="宗教词汇批量替换")
    parser.add_argument("target", help="文件路径或目录")
    parser.add_argument("--dry-run", action="store_true", help="预览，不修改文件")
    parser.add_argument("--audit-only", action="store_true", help="只做合规扫描，不替换、不写文件")
    parser.add_argument("--output-dir", default=str(OUTPUT_DIR), help="输出目录（默认：302.公众号洗稿）")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not args.dry_run and not args.audit_only:
        output_dir.mkdir(parents=True, exist_ok=True)

    target = Path(args.target)
    if target.is_file():
        process_file(target, args.dry_run, output_dir, args.audit_only)
    elif target.is_dir():
        # 目录模式：在输出目录下建同名子文件夹，保留相对路径结构
        dir_output = output_dir / target.name
        files = sorted(target.rglob("*.md"))
        print(f"找到 {len(files)} 个 .md 文件，输出至 {dir_output}\n")
        for f in files:
            rel = f.relative_to(target)
            dest_dir = dir_output / rel.parent
            if not args.dry_run and not args.audit_only:
                dest_dir.mkdir(parents=True, exist_ok=True)
            process_file(f, args.dry_run, dest_dir, args.audit_only)
    else:
        print(f"错误：找不到 {target}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
