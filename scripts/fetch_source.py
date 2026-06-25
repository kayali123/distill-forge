#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fetch_source.py — 抓取一个 URL 的原文,落盘到 <skill_dir>/references/sources/。
这是 provenance 指纹的地基:一手引用必须指向本次真实抓取的文件。
用法:  python fetch_source.py <url> --skill <skill_dir|slug>
输出:  {"relpath": "sources/<name>", "sha256": "...", "bytes": N}  (relpath 相对 references/)
"""
import sys, json, re, hashlib, argparse
from pathlib import Path
from urllib.request import Request, urlopen

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILLS_ROOT = Path.home() / ".claude" / "skills"

EXT_BY_TYPE = {
    "text/html": ".html", "text/plain": ".txt", "application/pdf": ".pdf",
    "application/json": ".json", "text/vtt": ".vtt", "application/x-subrip": ".srt",
}


def resolve_skill(arg: str) -> Path:
    p = Path(arg)
    if p.is_absolute() and p.exists():
        return p
    cand = SKILLS_ROOT / arg
    if cand.exists():
        return cand
    cand2 = SKILLS_ROOT / (arg if arg.endswith("-perspective") else f"{arg}-perspective")
    return cand2


def slugify(url: str) -> str:
    base = re.sub(r"^https?://", "", url)
    base = re.sub(r"[?#].*$", "", base)
    base = re.sub(r"[^A-Za-z0-9._-]+", "_", base).strip("_")
    return (base[:80] or "source")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--skill", required=True)
    ap.add_argument("--name", default=None, help="自定义文件名(不含扩展名)")
    args = ap.parse_args()

    skill = resolve_skill(args.skill)
    sources = skill / "references" / "sources"
    sources.mkdir(parents=True, exist_ok=True)

    try:
        req = Request(args.url, headers={"User-Agent": "Mozilla/5.0 distill-forge"})
        with urlopen(req, timeout=30) as resp:
            data = resp.read()
            ctype = (resp.headers.get_content_type() or "").lower()
    except Exception as e:
        print(json.dumps({"error": str(e), "url": args.url}, ensure_ascii=False))
        sys.exit(1)

    name = args.name or slugify(args.url)
    ext = EXT_BY_TYPE.get(ctype, "")
    if not ext:
        m = re.search(r"\.(html?|txt|pdf|json|srt|vtt|md)$", args.url, re.I)
        ext = ("." + m.group(1).lower()) if m else ".txt"
    if not name.endswith(ext):
        name += ext

    out = sources / name
    out.write_bytes(data)
    sha = hashlib.sha256(data).hexdigest()
    print(json.dumps({
        "relpath": f"sources/{name}", "abspath": str(out),
        "sha256": sha, "bytes": len(data), "content_type": ctype,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
