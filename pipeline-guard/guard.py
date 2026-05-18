#!/usr/bin/env python3
"""
pipeline-guard: 自动化流水线安全卫士

Three subcommands for safe multi-step automated workflows:
  filter  - Filter files before merging (exclude drafts, anchors, scene cards, etc.)
  scan    - Scan content for forbidden terms before external output
  clean   - Delete temp/draft files after work is done
"""

import sys, os, re, json, argparse
from pathlib import Path

# --- Default forbidden terms (real-world locations in fictional contexts) ---
DEFAULT_FORBIDDEN = [
    "深圳", "北京", "上海", "广州", "成都", "重庆", "武汉", "南京", "杭州",
    "中国", "地球", "美国", "日本", "英国", "法国", "德国", "俄罗斯", "韩国",
    "America", "Japan", "China", "England", "France", "Germany", "Russia",
]

DEFAULT_EXCLUDE_PATTERNS = [
    r"_tmp_",          # draft files
    r"_锚点",          # anchors
    r"_场景卡",        # scene cards
    r"_评分卡",        # rating cards
    r"_continuity",    # continuity check reports
    r"^_",             # any underscore-prefixed file
]


def fix_encoding():
    """Force UTF-8 output on Windows."""
    if hasattr(sys.stdout, 'reconfigure'):
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except Exception:
            pass


def cmd_filter(args):
    """Filter chapter files: given pattern, return only real body files."""
    d = Path(args.dir)
    if not d.is_dir():
        print(f"ERROR: not a directory: {d}", file=sys.stderr)
        sys.exit(1)

    pattern = args.pattern  # e.g. "第22章_*.md"
    all_matches = sorted(d.glob(pattern))

    exclude = DEFAULT_EXCLUDE_PATTERNS[:]
    if args.exclude_file:
        with open(args.exclude_file, encoding='utf-8') as f:
            exclude.extend([line.strip() for line in f if line.strip()])

    result = []
    skipped = []
    for f in all_matches:
        name = f.name
        if any(re.search(pat, name) for pat in exclude):
            skipped.append(name)
        else:
            result.append(f)

    if args.verbose:
        print(f"Pattern: {pattern}")
        print(f"Found:  {len(all_matches)} files")
        print(f"Kept:   {len(result)} files")
        if skipped:
            print(f"Skipped ({len(skipped)}): {', '.join(skipped)}")

    if not result:
        print("ERROR: no valid files matched after filtering", file=sys.stderr)
        sys.exit(1)

    if args.expect_one and len(result) != 1:
        print(f"ERROR: expected exactly 1 file, got {len(result)}: {[f.name for f in result]}", file=sys.stderr)
        sys.exit(1)

    for f in result:
        print(str(f))
    return 0


def cmd_scan(args):
    """Scan a file for forbidden terms."""
    path = Path(args.file)
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    content = path.read_text(encoding='utf-8')

    terms = DEFAULT_FORBIDDEN[:]
    if args.terms_file:
        with open(args.terms_file, encoding='utf-8') as f:
            terms.extend([line.strip() for line in f if line.strip() and not line.startswith('#')])

    hits = []
    for term in terms:
        positions = [m.start() for m in re.finditer(re.escape(term), content)]
        if positions:
            for pos in positions:
                # Extract context: 30 chars before and after
                start = max(0, pos - 30)
                end = min(len(content), pos + len(term) + 30)
                context = content[start:end].replace('\n', '↵')
                line_num = content[:pos].count('\n') + 1
                hits.append((term, line_num, context))

    ctx_label = args.context or path.stem

    if args.verbose and not hits:
        print(f"[{ctx_label}] ✅ Clean — no forbidden terms found ({len(terms)} terms checked)")

    if hits:
        print(f"[{ctx_label}] ❌ FOUND {len(hits)} FORBIDDEN TERM(S):")
        for term, line, ctx in hits:
            print(f"  Line {line}: 「{term}」 → ...{ctx}...")
        sys.exit(1)
    else:
        print(f"[{ctx_label}] ✅ PASSED")
        return 0


def cmd_clean(args):
    """Delete temp/draft files from a directory."""
    d = Path(args.dir)
    if not d.is_dir():
        print(f"ERROR: not a directory: {d}", file=sys.stderr)
        sys.exit(1)

    patterns = args.patterns or [
        r"_tmp_*.md",
        r"_init_*.py",
        r"_fix_*.py",
        r"_check_*.py",
        r"_find_*.py",
        r"_send_*.py",
        r"_sync_*.py",
        r"_verify_*.py",
        r"_read_*.py",
        r"_post_*.py",
        r"_apply_*.py",
        r"_record_*.py",
        r"_update_*.py",
        r"_search_*.py",
        r"_test_*.py",
        r"_cron_*.py",
        r"_*_chunk.txt",
        r"_*_result.txt",
    ]

    deleted = []
    for pat in patterns:
        for f in d.glob(pat):
            try:
                f.unlink()
                deleted.append(f.name)
            except OSError as e:
                print(f"WARN: could not delete {f.name}: {e}", file=sys.stderr)

    if args.verbose or deleted:
        if deleted:
            print(f"Cleaned {len(deleted)} temp file(s): {', '.join(deleted)}")
        else:
            print("Nothing to clean")
    return 0


def main():
    fix_encoding()

    parser = argparse.ArgumentParser(description="pipeline-guard: safety checks for automated workflows")
    sub = parser.add_subparsers(dest="command", required=True)

    # filter
    p = sub.add_parser("filter", help="Filter files before merging")
    p.add_argument("dir", help="Directory containing files")
    p.add_argument("pattern", help="Glob pattern, e.g. '第22章_*.md'")
    p.add_argument("--expect-one", action="store_true", help="Fail if != 1 file matches")
    p.add_argument("--exclude-file", help="Additional exclude patterns (one per line)")
    p.add_argument("-v", "--verbose", action="store_true")

    # scan
    p = sub.add_parser("scan", help="Scan content for forbidden terms")
    p.add_argument("file", help="File to scan")
    p.add_argument("--terms-file", help="Additional forbidden terms file")
    p.add_argument("--context", help="Label for output messages")
    p.add_argument("-v", "--verbose", action="store_true")

    # clean
    p = sub.add_parser("clean", help="Delete temp/draft files")
    p.add_argument("dir", help="Directory to clean")
    p.add_argument("--patterns", nargs="+", help="Glob patterns to delete")
    p.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    if args.command == "filter":
        cmd_filter(args)
    elif args.command == "scan":
        cmd_scan(args)
    elif args.command == "clean":
        cmd_clean(args)


if __name__ == "__main__":
    main()
