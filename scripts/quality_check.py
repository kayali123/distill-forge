#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""quality_check.py — provenance 指纹校验(优化项 #1)。
读 <skill_dir>/references/research/quotes.jsonl,对每条 tier="一手" 的引用,
核验其 span 确实(归一化后)出现在 references/<file> 里;否则记为应降级。
输出:claimed vs verified 一手数与占比、降级清单、各 model 源数。
用法:  python quality_check.py <skill_dir|slug>
"""
import sys, json, re, difflib, argparse
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILLS_ROOT = Path.home() / ".claude" / "skills"
FUZZY_THRESHOLD = 0.85
PUNCT = r"[\.,;:!\?\"'`’‘“”\(\)\[\]\{\}—\-–…、。，；：！？「」『』（）【】《》·]"


def resolve_skill(arg: str) -> Path:
    p = Path(arg)
    if p.is_absolute():
        return p
    for cand in (SKILLS_ROOT / arg,
                 SKILLS_ROOT / (arg if arg.endswith("-perspective") else f"{arg}-perspective")):
        if cand.exists():
            return cand
    return SKILLS_ROOT / arg


def norm(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"\s+", "", s)
    s = re.sub(PUNCT, "", s)
    return s


def span_in_file(span: str, filetext: str):
    ns, nt = norm(span), norm(filetext)
    if not ns:
        return False, 0.0
    if ns in nt:
        return True, 1.0
    sm = difflib.SequenceMatcher(None, ns, nt, autojunk=False)
    m = sm.find_longest_match(0, len(ns), 0, len(nt))
    cov = m.size / max(1, len(ns))
    return cov >= FUZZY_THRESHOLD, round(cov, 3)


def check(skill_dir) -> dict:
    skill = resolve_skill(str(skill_dir))
    refs = skill / "references"
    qpath = refs / "research" / "quotes.jsonl"
    report = {"skill_dir": str(skill), "quotes_file": str(qpath),
              "by_model": {}, "claimed_first_hand": 0, "verified_first_hand": 0,
              "total_quotes": 0, "downgrade": [], "errors": []}
    if not qpath.exists():
        report["errors"].append("quotes.jsonl 不存在")
        return report

    cache = {}
    for ln, raw in enumerate(qpath.read_text(encoding="utf-8").splitlines(), 1):
        raw = raw.strip()
        if not raw:
            continue
        try:
            q = json.loads(raw)
        except Exception as e:
            report["errors"].append(f"L{ln} 解析失败: {e}")
            continue
        report["total_quotes"] += 1
        model = q.get("model", "?")
        report["by_model"].setdefault(model, {"count": 0, "first_hand": 0})
        report["by_model"][model]["count"] += 1
        if q.get("tier") != "一手":
            continue
        report["claimed_first_hand"] += 1
        report["by_model"][model]["first_hand"] += 1

        rel = q.get("file", "")
        span = q.get("span", "")
        fpath = refs / rel if rel else None
        reason = None
        if not rel or not span:
            reason = "缺 file 或 span"
        elif fpath is None or not fpath.exists():
            reason = f"file 不存在: {rel}"
        else:
            if rel not in cache:
                cache[rel] = fpath.read_text(encoding="utf-8", errors="replace")
            ok, cov = span_in_file(span, cache[rel])
            if not ok:
                reason = f"span 未在 file 中找到 (coverage={cov})"
        if reason:
            report["downgrade"].append({"id": q.get("id", f"L{ln}"), "model": model,
                                        "reason": reason, "should_be": "推测"})
        else:
            report["verified_first_hand"] += 1

    cf, vf = report["claimed_first_hand"], report["verified_first_hand"]
    tot = report["total_quotes"]
    report["claimed_first_hand_ratio"] = round(cf / tot, 3) if tot else 0.0
    report["verified_first_hand_ratio"] = round(vf / tot, 3) if tot else 0.0
    report["fabrication_delta"] = cf - vf  # 声称一手 - 实证一手
    return report


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    args = ap.parse_args()
    print(json.dumps(check(args.skill), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
