#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_eval.py — 回放 eval 套件(优化项 #9)。
确定性部分自动跑(重算一手占比 vs baseline;若有样本则重算 DNA vs 容差带);
LLM 评判部分(sanity goldens / edge_case / 冷召回)打印成待 Claude 复判的清单。
用法:  python run_eval.py <skill_dir|slug>
样本(可选):<skill_dir>/references/eval/sample.txt  (人格输出样本,用于 DNA 回归)
"""
import sys, json, argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import quality_check  # noqa: E402
import expression_dna  # noqa: E402

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("skill")
    args = ap.parse_args()
    skill = quality_check.resolve_skill(args.skill)
    eval_path = skill / "references" / "eval" / "eval.json"
    if not eval_path.exists():
        print(json.dumps({"error": f"eval.json 不存在: {eval_path}"}, ensure_ascii=False))
        sys.exit(1)
    cfg = json.loads(eval_path.read_text(encoding="utf-8"))

    out = {"skill_dir": str(skill), "deterministic": {}, "needs_llm_review": {}}

    # 1) 一手占比回归
    qc = quality_check.check(skill)
    baseline = cfg.get("first_hand_ratio_baseline", 0.0)
    now = qc.get("verified_first_hand_ratio", 0.0)
    out["deterministic"]["first_hand_ratio"] = {
        "baseline": baseline, "now": now, "delta": round(now - baseline, 3),
        "fabrication_delta": qc.get("fabrication_delta"),
        "downgrade_count": len(qc.get("downgrade", [])),
    }

    # 2) DNA 容差带回归(需要样本)
    sample = skill / "references" / "eval" / "sample.txt"
    if sample.exists():
        metrics = expression_dna.dna(sample.read_text(encoding="utf-8", errors="replace"))
        bands = cfg.get("dna_targets", {})
        checks = {}
        out_of_band = 0
        for k, band in bands.items():
            v = metrics.get(k)
            if v is None or not isinstance(band, list) or len(band) != 2:
                checks[k] = {"value": v, "band": band, "status": "skip"}
                continue
            inb = band[0] <= v <= band[1]
            if not inb:
                out_of_band += 1
            checks[k] = {"value": v, "band": band, "status": "in" if inb else "OUT"}
        out["deterministic"]["dna"] = {"checks": checks, "out_of_band": out_of_band,
                                       "verdict": "ok" if out_of_band <= 1 else "drift(多指标漂移)"}
    else:
        out["deterministic"]["dna"] = {"note": "无 sample.txt,跳过 DNA 回归。把人格输出存到 references/eval/sample.txt 再跑。"}

    # 3) LLM 待判项
    out["needs_llm_review"]["sanity"] = cfg.get("sanity", [])
    out["needs_llm_review"]["edge_case_hedge"] = cfg.get("edge_case_hedge", "")
    out["needs_llm_review"]["cold_recall_note"] = (
        "fame_tier=high 时,让独立无工具 agent 凭记忆复现关键引用与立场;能复现的标污染。"
        if cfg.get("fame_tier") == "high" else "fame_tier 非 high,冷召回非必须。")

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
