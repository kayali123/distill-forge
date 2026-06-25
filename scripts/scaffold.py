#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""scaffold.py — Phase 0.5: 先建目标 skill 的目录树。
用法:  python scaffold.py <slug>
生成:  ~/.claude/skills/<slug>-perspective/  (含 references/research, sources, eval 与占位文件)
"""
import sys, json, io
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILLS_ROOT = Path.home() / ".claude" / "skills"

RESEARCH_FILES = ["01-著作.md", "02-对话.md", "03-表达.md",
                  "04-他者.md", "05-决策.md", "06-时间线.md"]

EVAL_STUB = {
    "target": "<name>",
    "research_date": "YYYY-MM-DD",
    "fame_tier": "mid",
    "first_hand_ratio_baseline": 0.0,
    "sanity": [{"q": "", "golden_stance": "", "source_path": ""}],
    "edge_case_hedge": "",
    "dna_targets": {
        "avg_sentence_len": [12, 22], "interrogative_ratio": [0.0, 0.15],
        "analogy_per_1k": [1, 6], "first_person_ratio": [0.0, 0.3],
        "certainty_ratio": [0.1, 0.5], "transition_per_1k": [2, 12],
    },
    "cold_recall_contaminated": [],
    "weakness_record": {},
}

SKILL_STUB = """---
name: {slug}-perspective
description: 用「{slug}」的视角/思维方式看问题。触发:用{slug}的视角、{slug} perspective、切换到{slug}。不要在询问<填负向触发>时触发。
research_date: YYYY-MM-DD
refresh_interval_days: 90
target_type: person
use_case: advisor
target_class: public-figure
consent_basis: N/A
fame_tier: mid
---

<!-- 由 distill-forge 在 Phase 3 填充。请勿手填,走流程生成。 -->
"""


def main():
    if len(sys.argv) < 2:
        print("用法: python scaffold.py <slug>", file=sys.stderr)
        sys.exit(2)
    slug = sys.argv[1].strip().rstrip("/").replace(" ", "-")
    if slug.endswith("-perspective"):
        slug = slug[: -len("-perspective")]
    skill = SKILLS_ROOT / f"{slug}-perspective"
    refs = skill / "references"
    dirs = [skill, refs, refs / "research", refs / "sources", refs / "eval"]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 占位文件(不覆盖已存在的)
    created = []
    def write_if_absent(path: Path, content: str):
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            created.append(str(path))

    write_if_absent(skill / "SKILL.md", SKILL_STUB.format(slug=slug))
    for f in RESEARCH_FILES:
        write_if_absent(refs / "research" / f, f"# {f[:-3]}\n\n<!-- 引用同时写进 quotes.jsonl -->\n")
    write_if_absent(refs / "research" / "quotes.jsonl", "")
    write_if_absent(refs / "research" / "exclusivity-baseline.md",
                    "# 排他性盲测基线\n\n<!-- 盲 agent 的通才答案 vs 候选模型的分歧 -->\n")
    write_if_absent(refs / "research-protocol.md",
                    "# Agentic Protocol\n\n| 心智模型 | 触发的问题类型 | 具体搜索维度 |\n|---|---|---|\n")
    write_if_absent(refs / "eval" / "eval.json",
                    json.dumps(EVAL_STUB, ensure_ascii=False, indent=2))

    print(f"已创建 skill 目录: {skill}")
    print("树:")
    for p in sorted(skill.rglob("*")):
        rel = p.relative_to(skill)
        indent = "  " * (len(rel.parts) - 1)
        mark = "/" if p.is_dir() else ""
        print(f"  {indent}{p.name}{mark}")
    print(f"\n新建文件 {len(created)} 个(已存在的未覆盖)。")
    print(json.dumps({"skill_dir": str(skill)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
