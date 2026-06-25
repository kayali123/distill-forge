---
name: distill-forge
description: >-
  通用「人物蒸馏」meta-skill——把任何人(从资料海量的名人,到只有零星访谈的小众高手)的认知操作系统蒸馏成一个可复用、可重跑、带置信度与溯源的「视角 skill」。
  触发词:「蒸馏XX」「造一个XX的skill」「把XX蒸馏成skill」「XX的思维方式」「用XX的视角」「更新XX的skill」「重新验证XX」「distill XX」;
  以及模糊需求「我想提升某类决策」「我需要一个思维顾问」(此时先反推该蒸馏谁)。
  与 nuwa-skill 的差异:以反幻觉(provenance 指纹)、数据稀疏自适应、伦理/consent 闸门、advisor/roleplay 双模式、可重跑 eval 为核心。
---

# distill-forge · 通用人物蒸馏

把"一个人怎么思考"提炼成一个能跑的 skill。不是 cosplay,而是抽取**认知操作系统**:心智模型、决策启发、表达指纹、价值边界、诚实局限。

> **最高原则:标注了局限的诚实 60 分,胜过看起来 90 分的伪造品。**
> 蒸馏的死穴是 AI 凭训练记忆"造人格"。本工具的存在理由就是**强制溯源 + 诚实置信度**。

---

## 何时触发
- 显式:`蒸馏马斯克` / `造一个芒格的skill` / `用纳瓦尔的视角看X` / `更新X的skill` / `重新验证X`。
- 模糊:`我想提升投资决策质量` → 走 **Phase 0B** 反推该蒸馏谁(给 ≤3 个差异化候选,本地已装的 skill 优先列出),不要替用户硬选。

---

## 总流程(0 → 5,阶段间有"人来点头"的闸门)

```
0 路由 ─┬─ 显式名 ──→ 0A 配置澄清(who/focus/use_case/target_type/新建or更新/有无一手语料)
        └─ 模糊需求 → 0B 反推目标(≤2 轮提问 → ≤3 候选)
0A 顺带做三件分类:fame_tier(数据密度) · target_class(伦理) · refresh_interval(时间敏感)
0.5 scaffold.py 先建目录树   ← 铁律:没写进文件的调研 = 没做
1  六路并行采集(著作/对话/表达/他者/决策/时间线),一手必须落盘到 sources/
1.5 ▣ 评审闸:展示「声称一手 vs 实证一手」差值 + 黑名单豁免项,人批准
2  三重验证合成框架(排他性走对比式盲测)
2.5 ▣ 合成确认闸
3  构建 SKILL.md(按 use_case 选 roleplay/advisor 模板)+ 注入 Agentic Protocol + 写 frontmatter + eval.json
4  验证(独立 sub-agent:检索锚定 sanity + 冷召回污染测试 + DNA 软信号 + 派生维度断言)
5  双 agent 精修(结构 + 可操作性)+ 人确认
( Phase 2↔4 返工最多 2 轮;到顶就带 weakness_record 诚实发车 )
```

---

## Phase 0 — 路由 + 配置

### 0A 配置澄清(显式目标)
一轮问清并记录为变量(后续所有阶段都读这些变量,**不要硬编码"变成那个人"**):

| 变量 | 取值 | 用途 |
|---|---|---|
| `target` | 人名 | — |
| `focus` | 一句话(如"投资决策"/"产品审美") | 收窄采集 |
| `use_case` | `roleplay` / `advisor` / `decision-reference` | Phase 3 选模板头 |
| `target_type` | `person`(默认) / `methodology`(预留) | 采集与验证维度 |
| `mode` | `new` / `update` | update 只重跑 agent 2/5/6 |
| `has_corpus` | 用户是否有一手本地语料(PDF/字幕/截图) | 有则优先喂入 |

**同一轮顺带三项分类(决定后面的闸门强度):**
- **`fame_tier`**(数据密度):`high`(全球级名人,预训练覆盖海量)/ `mid`(有少量访谈/播客)/ `low`(资料稀疏的小众高手)。见下方"自适应规则"。
- **`target_class`**(伦理):`public-figure` / `semi-public` / `private-individual` / `deceased`。按 `references/ethics-routing.md` 处理。
- **`refresh_interval_days`**:活跃公众人物→短(如 90);历史/逝者→长或留空。

### 0B 反推目标(模糊需求)
按 `references/extraction-framework.md` 的 need→framework 表反推;≤2 轮提问;给 ≤3 个差异化候选(每个标 核心视角 / 为何适合 / 局限);**本地已装的 `*-perspective` skill 优先展示**,避免重复造。

---

## Phase 0.5 — 先建目录(铁律)
```
python scripts/scaffold.py <target-slug>
```
生成自包含的目标 skill 目录(见末尾"生成物结构")。**所有调研产物必须写进这个目录**——这是开源可分发 + 可验证的前提。

---

## Phase 1 — 六路并行采集
spawn 6 个并行 sub-agent,各产一个文件,各自只管一个维度:

| Agent | 文件 | 抓什么 |
|---|---|---|
| 1 著作 | `references/research/01-著作.md` | 本人书/长文/署名文章里的原话 |
| 2 对话 | `references/research/02-对话.md` | 访谈/播客/演讲的逐字(用字幕,清洗后) |
| 3 表达 | `references/research/03-表达.md` | 社媒/短发言,抓句式口头禅 |
| 4 他者 | `references/research/04-他者.md` | 别人对他的记述、他对具体问题的已知立场 |
| 5 决策 | `references/research/05-决策.md` | 关键决策记录(做过什么、放弃过什么) |
| 6 时间线 | `references/research/06-时间线.md` | 近 12 个月动态(供时间敏感判断) |

**采集纪律(对应已验证优化项):**
- **每条引用都进 `references/research/quotes.jsonl`**(机读,见下方"约定/CONTRACT")。一手(`tier:"一手"`)**必须**带 `file`(指向本次抓取并落盘到 `references/sources/` 的真实文件)+ `span`(该文件里真实出现的逐字片段)。**断言的 URL 不算一手。**
- 落盘用 `python scripts/fetch_source.py <url> --skill <skill_dir>`,它把原文存进 `sources/` 并回传相对路径 + sha256。字幕用 `srt_clean.py` 清洗。
- **来源 provenance-first**(见 `references/source-gating.md`):知乎/公众号/百度默认拒,但"作者自有可验证渠道"例外(标 `blacklisted-host-but-author-owned`);白名单媒体不享受无条件可信,每篇仍标一手/二手。
- 优先调用已装的信息获取 skill(如 deep-research / arxiv / web-article-reader / pdf),而非裸搜。
- **数据稀疏自适应**:见下。超时(单源卡 5 分钟)→ 跳过并标边界。

### 数据密度自适应规则(本工具对 nuwa 的关键升级)
| `fame_tier` | 心智模型上限 | 一手占比闸门 | 额外动作 |
|---|---|---|---|
| `high` | 5-7 | **>70%** | Phase 4 强制跑**冷召回污染测试**(见下) |
| `mid` | 3-5 | >50% | 标准 |
| `low` | **2-3** | 尽力,无硬闸 | `honest boundaries` 里写明"基于 N 条素材/X 条一手,置信度=低";措辞普遍更保守 |

---

## Phase 1.5 — ▣ 评审闸(人来点头)
运行 `python scripts/quality_check.py <skill_dir>`,展示:
- 各维度源数量;**声称一手 vs 实证一手(span 核验通过)的差值** ← 让用户在合成前就看到造假风险;
- 所有 blacklist 豁免项;低源警告。
用户批准后才进 Phase 2。

---

## Phase 2 — 三重验证 + 合成
按 `references/extraction-framework.md`:
- **复现性**(跨领域 ≥2)+ **生成力**(能推出对新问题的非平凡判断)+ **排他性** → 3/3=心智模型,1-2=降级为决策启发,0=丢弃。
- **排他性走对比式盲测**:对已过前两关的候选,spawn 一个**只给问题、不给候选模型、不给人名**的盲 agent 产"通才答案";候选须在多数测试题上给出**更具体且不同**的判断,并写一行"分歧在哪、为何"才算过;说不出具体分歧 → 降级。盲基线落盘到 `references/research/exclusivity-baseline.md`。
- 再抽:决策启发(5-10)、**表达 DNA**(用 `expression_dna.py` 算 6 句法指标 + 7 风格轴,落成容差带)、价值观与反模式(保留内部张力)、思想谱系、诚实边界。

## Phase 2.5 — ▣ 合成确认闸

---

## Phase 3 — 构建目标 SKILL.md
- **按 `use_case` 选模板头**:
  - `roleplay` → `references/skill-template.roleplay.md`(第一人称沉浸,角色扮演规则最重要)。
  - `advisor` / `decision-reference` → `references/skill-template.advisor.md`(第三人称,**显式亮出**用了哪个心智模型 + 哪条启发 + 针对此问题的局限)。
  - **伦理默认**:`private-individual` / `semi-public` 默认强制 advisor 模式,除非用户带 consent 显式选 roleplay(见 `ethics-routing.md`)。
- 共享体见模板文件。
- **注入 Agentic Protocol**:把"心智模型 → 触发的问题类型 → 具体搜索维度"落成 `references/research-protocol.md`(由 `research-protocol.template.md` 实例化),SKILL.md 引用它而非内联散文。激活时:`今天 − research_date > refresh_interval_days` 则在答案前加一行陈旧声明。
- **写 frontmatter(单一真相源)**:
```yaml
name: <slug>-perspective
description: <含人名 token 的触发 + 一行负向触发,如"不要在询问烹饪/医疗时触发">
research_date: <YYYY-MM-DD>        # 构建时戳(从环境取当天日期)
refresh_interval_days: <int>
target_type: person
use_case: roleplay|advisor|decision-reference
target_class: public-figure|semi-public|private-individual|deceased
consent_basis: <一行 或 N/A>
fame_tier: high|mid|low
```
- **落 `references/eval/eval.json`**(见 CONTRACT)。

---

## Phase 4 — 验证(独立 sub-agent)
- **检索锚定 sanity**:对 3 个已知立场问题,验证 agent 必须先从 `04-他者.md` / `sources/` **逐字引用**目标真实立场(带可信度标签),只拿生成答案跟这条落盘引用比;查无佐证 → 记 `ungrounded/cannot-verify`,不算过。**硬失败**:sanity 通过但匹配立场无落盘佐证(抓互相幻觉)。
- **冷召回污染测试(仅 `fame_tier=high`)**:独立无工具 agent 凭记忆复现关键引用 + 3-5 条蒸馏立场。能凭记忆复现的 → 标"预训练污染/来源不可验",须有一手佐证否则降级。**整套人格在没有蒸馏语料时就能被重建 = 验证失败,触发返工。**
- **DNA 软信号**:`expression_dna.py` 在 100 词样本上算指标,报告偏离容差带的项;**仅当多指标显著漂移才算真失误**(单短样本不做硬 pass/fail)。
- **派生维度断言**:对一个需事实的探针,断言答案确实触发了该人格的特定派生维度(如芒格 skill 须触发"激励/逆向"搜索)。
- **跨模型(尽力)**:口吻/立场检查尽量走不同模型家族;无第二模型则标 `single-model, unverified for prior bias`,不谎称独立。
- 终极判据"去名识别"保留,但从唯一裁判**降级为一个信号**(对名人它分不清语料保真 vs 预训练记忆)。
- Phase 2↔4 返工上限 2;到顶带 `weakness_record` 诚实发车。

---

## Phase 5 — 双 agent 精修 + 确认
结构优化器(可读性/层次)+ 可操作性评审(触发器/边界/能否真跑)→ 合并 → 人确认。

---

## Update 模式(`mode=update`)
- 只重跑 agent 2/5/6(对话/决策/时间线);reconcile 时读 frontmatter 的 `research_date`/`refresh_interval_days`(**不要正则抠散文**);完成后戳新 `research_date`。
- DNA 容差带 + `research-protocol.md` 作结构化对账锚。
- **完成后强制 `python scripts/run_eval.py <skill_dir>` 回放 eval 套件**,并排展示 new vs golden 供人审。

---

## 打包发布
```bash
cd ~/.claude/skills/<slug>-perspective
git init && git add . && git commit -m "distilled <name> perspective"
gh repo create <slug>-perspective --public --source=. --push
# 他人安装:  npx skills add github:<you>/<slug>-perspective
```
发布前清单:frontmatter 含人名 token + 负向触发;`target_class`/`consent_basis` 已填;`sources/` 有真实文件;`eval/eval.json` 存在。不做技术性"再分发剥离"(开源 SKILL.md 无法强制),靠 metadata + 一行 caveat。

---

## 生成物结构(scaffold.py 产出)
```
~/.claude/skills/<slug>-perspective/
├── SKILL.md
└── references/
    ├── research/
    │   ├── 01-著作.md … 06-时间线.md
    │   ├── quotes.jsonl              # 所有引用(机读,quality_check 读它)
    │   └── exclusivity-baseline.md   # 排他性盲测基线
    ├── sources/                      # 本次真实抓取的原文件(provenance 锚)
    ├── research-protocol.md          # Agentic Protocol 表
    └── eval/
        └── eval.json                 # 回归套件
```

---

## 约定 / CONTRACT(所有脚本与文件必须遵守)

### A. `references/research/quotes.jsonl` —— 每行一个 JSON 对象
```json
{"id":"q001","model":"01-著作","tier":"一手","text":"完整引用原文","source":"来源可读名称","file":"sources/2019_interview.txt","span":"必须逐字出现在 file 里的片段","lang":"zh","date":"2019"}
```
- `tier` ∈ `一手` | `二手` | `推测`。
- `tier=="一手"` 时 `file` 与 `span` **必填**;`quality_check.py` 归一化(去空白/标点差异)后核验 `span` 确在 `references/<file>` 中出现,否则该条**自动降级为 `推测`**。
- 翻译材料:`lang` 标源语言,`span` 用源语言片段。

### B. `references/eval/eval.json`
```json
{
  "target": "<name>",
  "research_date": "YYYY-MM-DD",
  "fame_tier": "high|mid|low",
  "first_hand_ratio_baseline": 0.72,
  "sanity": [{"q": "问题", "golden_stance": "落盘佐证的真实立场", "source_path": "sources/xx.txt"}],
  "edge_case_hedge": "一个他从未公开谈过的问题(期望得到对冲/不确定的回答)",
  "dna_targets": {"avg_sentence_len":[12,22],"interrogative_ratio":[0.0,0.15],"analogy_per_1k":[1,6],"first_person_ratio":[0.0,0.3],"certainty_ratio":[0.1,0.5],"transition_per_1k":[2,12]},
  "cold_recall_contaminated": [],
  "weakness_record": {}
}
```

### C. 脚本 CLI(全部纯标准库,Windows 可跑)
- `scaffold.py <slug>` → 建 `~/.claude/skills/<slug>-perspective/` 全树,打印树。
- `fetch_source.py <url> --skill <skill_dir>` → 存原文到 `<skill_dir>/references/sources/`,打印 `{relpath, sha256, bytes}`。
- `srt_clean.py <in.srt> [--out file]` → 去时间轴/序号/去重,输出纯文本。
- `quality_check.py <skill_dir>` → 读 `quotes.jsonl`,核验每条一手的 span,打印 JSON 报告(claimed vs verified 一手数与占比、降级清单)。
- `expression_dna.py <textfile|-> ` → 打印 6 指标 JSON(avg_sentence_len / interrogative_ratio / analogy_per_1k / first_person_ratio / certainty_ratio / transition_per_1k)。
- `run_eval.py <skill_dir>` → 读 `eval/eval.json`,跑确定性项(重算一手占比、若给样本则重算 DNA 并比对容差带),打印报告 + 标出需 LLM 复判的项。

### D. 路径解析
脚本一律用 `pathlib.Path.home()/".claude"/"skills"` 定位 skills 根;接受 `<skill_dir>` 为绝对路径或 slug(自动补全)。

---

_本 meta-skill 由 distill-forge 生成体系产出。生成的每个目标 skill 应在 footer 注明:基于公开记录蒸馏,非本人真实观点;并随附 target_class / consent_basis 出处。_
