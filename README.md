# distill-forge · 通用人物蒸馏 Skill

把**任何人**(从资料海量的名人,到只有零星访谈的小众高手)的「认知操作系统」——心智模型、决策逻辑、表达指纹、价值边界、诚实局限——从公开资料里系统化提取,生成一个**可复用、可重跑、带置信度与溯源**的「视角 skill」。

> **最高原则:标注了局限的诚实 60 分,胜过看起来 90 分的伪造品。**
> 蒸馏的死穴是 AI 凭训练记忆「造人格」。本工具的存在理由,就是**强制溯源 + 诚实置信度**。

本项目受 [alchaincyf/nuwa-skill](https://github.com/alchaincyf/nuwa-skill) 启发,并在其基础上做了一套以**反幻觉**为核心的重构。

---

## 它和 nuwa-skill 的差异(核心升级)

| | nuwa-skill | distill-forge |
|---|---|---|
| **反幻觉** | 由 agent 自报「一手」,可被编造 | **provenance 指纹**:一手引用必须绑定本次抓取的真实文件 + 逐字 `span`,`quality_check.py` 自动核验,对不上的降级为「推测」 |
| **任何人** | 示例全是预训练海量覆盖的名人 | **`fame_tier` 数据密度自适应**:名人端加冷召回防污染;小众高手端诚实标低置信度 |
| **有用性** | 硬编码「变成那个人」 | **`use_case` 双模板**:roleplay(沉浸第一人称)/ advisor(第三人称,显式亮出 模型+启发+局限) |
| **伦理** | 一句免责声明 | **`target_class` + consent 闸门**:私人/逝者特殊处理,元信息随 skill 流通 |
| **生命周期** | 构建时验一次 | **可重跑 eval**:`run_eval.py` 在 update / 换宿主模型后查人格漂移 |

---

## 安装

```bash
# 跨 runtime(Claude Code / Cursor / Codex 等)
npx skills add github:kayali123/distill-forge
```

或手动:把本仓库放到 `~/.claude/skills/distill-forge/`(Windows:`C:\Users\<你>\.claude\skills\distill-forge\`)。

## 用法

直接说触发词,整条流水线会按 `SKILL.md` 一阶段一阶段走(关键节点停下来让你确认):

```
蒸馏 <某人>
造一个 <某人> 的 skill
用 <某人> 的视角看 <某问题>
更新 <某人> 的 skill / 重新验证 <某人>
```

模糊需求(如「我想提升投资决策」)会先反推「该蒸馏谁」,给 ≤3 个候选。

---

## 工作流(0 → 5)

```
0 路由 → 0A 配置(use_case / target_type / fame_tier / target_class / 时间敏感)
0.5 scaffold.py 先建目录(铁律:没写进文件的调研 = 没做)
1  六路并行采集(著作/对话/表达/他者/决策/时间线),一手必须落盘到 sources/
1.5 ▣ 评审闸:展示「声称一手 vs 实证一手」差值,人批准
2  三重验证合成框架(排他性走对比式盲测)
2.5 ▣ 合成确认闸
3  构建 SKILL.md(按 use_case 选模板)+ Agentic Protocol + frontmatter + eval.json
4  验证(检索锚定 sanity + 冷召回污染测试 + DNA 软信号 + 派生维度断言)
5  双 agent 精修 + 人确认
```

## 目录结构

```
distill-forge/
├── SKILL.md                          # 编排器(含「约定 / CONTRACT」)
├── references/
│   ├── extraction-framework.md       # 三重验证 + 五层提取 + 需求反推表 + fame_tier 自适应
│   ├── skill-template.roleplay.md    # 沉浸第一人称输出模板
│   ├── skill-template.advisor.md     # 第三人称顾问输出模板
│   ├── ethics-routing.md             # target_class 四分类 + consent 闸门
│   ├── source-gating.md              # provenance-first 来源闸门
│   └── research-protocol.template.md # 运行时按心智模型派生搜索维度
└── scripts/                          # 纯标准库 Python,Windows/py3 可跑
    ├── scaffold.py        # 建自包含目录树
    ├── fetch_source.py    # 抓原文落盘(provenance 锚)
    ├── quality_check.py   # ★ 一手引用 span 指纹校验
    ├── expression_dna.py  # 6 个表达指纹指标
    ├── run_eval.py        # 可重跑回归套件
    └── srt_clean.py       # 字幕清洗
```

---

## 伦理

生成的每个「视角 skill」基于**公开记录**蒸馏,**不代表本人真实观点**,并随附 `target_class` / `consent_basis` 出处。请勿用于冒充、骚扰或误导。

## 致谢

灵感来自 [@alchaincyf](https://github.com/alchaincyf) 的 [nuwa-skill](https://github.com/alchaincyf/nuwa-skill)。

## License

MIT
