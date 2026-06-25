#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""srt_clean.py — 清洗字幕(.srt/.vtt):去序号、去时间轴、去连续重复行,合并为纯文本。
用法:  python srt_clean.py <in.srt> [--out out.txt]
不给 --out 时打印到 stdout。
"""
import sys, re, argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TS = re.compile(r"^\s*\d{1,2}:\d{2}:\d{2}[.,]\d{1,3}\s*-->")
IDX = re.compile(r"^\s*\d+\s*$")
TAG = re.compile(r"<[^>]+>")


def clean(text: str) -> str:
    out, prev = [], None
    for line in text.splitlines():
        s = line.strip()
        if not s or s.upper().startswith("WEBVTT") or TS.match(s) or IDX.match(s):
            continue
        s = TAG.sub("", s).strip()
        if not s or s == prev:
            continue
        out.append(s)
        prev = s
    # 合并:中文不加空格,其余加空格
    joined = ""
    for seg in out:
        if joined and not re.search(r"[一-鿿]$", joined):
            joined += " "
        joined += seg
    return joined


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("infile")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    text = Path(args.infile).read_text(encoding="utf-8", errors="replace")
    result = clean(text)
    if args.out:
        Path(args.out).write_text(result, encoding="utf-8")
        print(f"已写出: {args.out}  ({len(result)} 字符)")
    else:
        print(result)


if __name__ == "__main__":
    main()
