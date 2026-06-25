# ethics-routing —— 伦理 / consent 路由(优化项 #7)

本文件定义 `target_class` 四分类、consent 闸门、默认模式翻转、逝者/弱势的 dignity 处理,以及把这套折叠进 **Phase 0A** 澄清提问的话术。

由 `SKILL.md` 的 Phase 0A 引用:`target_class` 在配置澄清那一轮顺带判定,结果写进目标 skill 的 frontmatter(`target_class` + `consent_basis`),并影响 Phase 3 的模板选择(`use_case`→roleplay/advisor)。

> **本工具的最高原则同样适用于伦理:宁可拒绝/降级,不要在没有正当理由时蒸馏一个能被认出的真人。**
> 蒸馏越逼真,对**非公众人物**的伤害越大。`target_class` 的作用是:名气越小、越私人 → 闸门越严。

---

## 1. `target_class` 四分类表

在 Phase 0A 判定。判定看的是**目标这个人**(不是资料多少——那是 `fame_tier` 管的事)。两者正交:一个 `fame_tier=low` 的小众高手,完全可能是 `public-figure`(公开出书/上播客就是公开自我表达);一个 `fame_tier=mid` 的人也可能是 `private-individual`(你朋友、你导师)。

| `target_class` | 判定标准 | 主要风险 | 处理动作(默认) |
|---|---|---|---|
| `public-figure` | 主动且持续地公开自我表达:公职/企业高管、作家、有公开作品或大量受访记录的创作者;其言行本就供公众评议。 | 名誉/语境失真为主;肖像权、人格权风险低(已自愿进入公共讨论)。 | 正常走全流程;无需 consent 闸。`use_case` 由用户选。footer 标"基于公开记录蒸馏,非本人真实观点"。 |
| `semi-public` | 有一定公开足迹但**非**主动公众人物:小范围 KOL、行业内知名但圈外无名、只有零星访谈/会议发言的人;公开度不足以默认其同意被"建模"。 | 隐私 + 人格权(personality rights);被放大、被代言其未表态立场;publicity rights(肖像/姓名商业化)。 | **触发 consent 闸**(见 §2);**默认强制 advisor 模式**(见 §3);无 consent 则拒绝或仅做 advisor。 |
| `private-individual` | 普通个人:用户的朋友/同事/家人/导师、未公开的私人对话对象;基本无公共足迹。 | 隐私权 + 肖像权 + 人格权,风险最高;几乎一定缺乏"被公开建模"的同意;可能涉私密信息。 | **强制 consent 闸**(见 §2),无确认**直接拒绝**;有 consent 也**默认强制 advisor**;素材必须用户自有合法来源。 |
| `deceased` | 已故者(无论生前公开度)。 | 无法本人同意;后人/遗产的人格利益(部分法域有死后人格权/postmortem publicity rights);失真传播;对在世亲属的情感伤害。 | 强制在"诚实边界"写 **dignity note**(见 §4);若逝者生前为 `private-individual` 量级,叠加 §2 的 consent 闸(由在世亲属/合法权利人确认)。 |

判定边界提示:
- 拿不准 `public-figure` 还是 `semi-public` → **就低判 `semi-public`**(更严的闸不会错杀,漏判才会伤人)。
- "在某垂直社区很有名" ≠ `public-figure`;要看其是否**主动公开自我表达**且有可验证的公开渠道。
- 同一个人可能跨界:某高管的"公司决策"是 public,其"私人育儿观"可能是 private——以 `focus` 收窄后的那一面定 class。

---

## 2. consent 闸门

适用 `target_class ∈ {private-individual, semi-public}`(以及生前为该量级的 `deceased`)。

**闸门动作:** 在 Phase 0A 末尾、进入 Phase 0.5 建目录**之前**,要求用户给出**一行确认**:声明其"**有授权或正当理由**"蒸馏此人,并说明依据。把这一行原样(可压成一句)写进目标 frontmatter 的 `consent_basis`。

### 话术(直接问用户)

> `<target>` 我判定为 **`<target_class>`**(非主动公众人物 / 私人个体)。蒸馏一个能被认出的真人需要正当理由。请用一行确认其一:
> (a) 本人已授权;
> (b) 你与本人的关系 + 用途使其属正当(如自用复盘、对方知情同意);
> (c) 素材全部来自你**合法持有**的一手语料(你们的往来记录/对方给你的材料),仅供你**个人**参考。
> 不确认我就**只能拒绝或退到 advisor(顾问)模式、不做第一人称扮演**。

### 写入 frontmatter

确认后,`consent_basis` 写成一行可追溯说明,例如:

```yaml
target_class: private-individual
consent_basis: "用户为本人前同事,自用决策复盘;素材为双方邮件/聊天记录(用户合法持有);2026-06-25 用户书面确认"
```

未触发闸门的 `public-figure` 写:

```yaml
target_class: public-figure
consent_basis: N/A
```

### 无确认时的两条出路

| 情形 | 动作 |
|---|---|
| `private-individual` 且用户**给不出**任何 (a)/(b)/(c) | **拒绝**。不建目录、不采集。一句话说明:私人个体未经授权不蒸馏。 |
| `semi-public` 给不出明确授权,但有合理自用理由 | **不拒绝,但强制 advisor**:`consent_basis` 标 `"无显式授权;限 advisor 自用;基于公开记录"`,且 §3 的 advisor 锁定不可被 roleplay 覆盖。 |

> consent 是**人工闸门**,与 Phase 1.5 的评审闸性质一致:脚本不替用户判断"正当理由",只负责把 `consent_basis` 落进 frontmatter 并在发布前清单校验其非空。

---

## 3. 默认模式翻转(use_case override)

正常情况下 `use_case` 由用户在 Phase 0A 选。但伦理路由会**翻转默认值**:

| `target_class` | `use_case` 默认 | 能否选 `roleplay` |
|---|---|---|
| `public-figure` | 用户自选(无强制) | 可 |
| `semi-public` | **强制 `advisor`** | 仅当**带 consent 且用户显式要求** roleplay 才解锁 |
| `private-individual` | **强制 `advisor`** | 仅当**带 consent 且用户显式要求** roleplay 才解锁 |
| `deceased`(生前 private 量级) | **强制 `advisor`** | 需权利人 consent + 显式要求 |

机制:
- Phase 0A 判完 `target_class` 后,若属上表强制行,**先把 `use_case` 落为 `advisor`**(覆盖用户的初始选择),并告知用户为何翻转。
- 解锁 `roleplay` 的唯一路径:`consent_basis` 非 N/A **且** 用户在被告知风险后**显式**说"要第一人称扮演"。此时 Phase 3 才允许选 `references/skill-template.roleplay.md`,否则一律 `references/skill-template.advisor.md`。
- 这条与 SKILL.md Phase 3 的"伦理默认"一致:advisor 模板**显式亮出**用了哪个心智模型 / 哪条启发 / 针对此问题的局限——这本身就是对非公众人物更安全的呈现方式(不冒充其口吻、不替其表态)。

advisor 锁定时的一行风险告知话术:

> 因为 `<target>` 是 `<target_class>`,我默认用 **advisor(第三人称顾问)** 模式:亮出推理依据而非模仿其口吻,避免替真人"代言"。要切到第一人称扮演,需要你确认有授权并显式要求。

---

## 4. 逝者 / 弱势 —— 强制 dignity note

适用:`target_class == deceased`;以及任何虽在世但处弱势/易受伤害的情形(重病、未成年、受公共争议或污名、无力回应者)。

**强制动作:** 在目标 skill 的**诚实边界(honest boundaries)**段落里写一条 **dignity note**。这是诚实边界的一部分,不是免责声明走过场。它必须:点明这是蒸馏品而非本人、标注局限、不替逝者/弱势者对其生前未表态的新问题"代言"。

### dignity note 模板句(按 class 选用 / 改写)

**逝者(deceased):**
> 本 skill 基于 `<target>` 的公开记录蒸馏,**非本人、本人已无法确认或修正任何观点**。对其生前未公开谈及的问题,只给"基于其已知思想谱系的审慎推测",并显式标注不确定;不杜撰立场、不替其对身后之事表态。请以纪念与尊重待之。

**生前为私人个体的逝者(deceased + 经权利人 consent):**
> 本 skill 由 `<在世权利人关系>` 在知情同意下,基于其合法持有的一手材料蒸馏,仅供 `<用途>`。`<target>` 已故,无法本人确认;任何超出留存材料的内容均为推测并如此标注。

**在世弱势者:**
> `<target>` 当前处于 `<情形>`。本 skill 不模仿其口吻、不替其对私人/敏感议题表态;仅在其**已公开**的范围内提供审慎参考,边界之外一律对冲。

写入位置:目标 SKILL.md 的"诚实边界"小节(advisor 模板该小节天然存在);并在 footer 复述一行(与 SKILL.md footer 约定一致:基于公开记录蒸馏,非本人真实观点 + 随附 `target_class` / `consent_basis` 出处)。

---

## 5. 使用 caveat(随 skill 分发)

> **caveat(写进每个目标 skill 的 footer):** 本工具**不做技术性"再分发剥离"**——开源的 SKILL.md 无法在代码层强制谁能用、怎么用;伦理边界靠 frontmatter 的 `target_class` / `consent_basis` **metadata 标注**与本 caveat 声明承载,使用者有责任在其自身正当授权范围内使用。

(与 SKILL.md「打包发布」一节口径一致:不做技术性再分发剥离,靠 metadata + 一行 caveat。)

---

## 6. 折叠进 Phase 0A 的澄清提问(话术)

把伦理判定**并进** Phase 0A 那一轮,不额外加轮次。在问 who/focus/use_case/target_type/new-or-update/has_corpus 的同时,顺带定 `fame_tier`(数据密度)/ `target_class`(伦理)/ `refresh_interval_days`(时间敏感)。伦理那一问的标准话术:

> 关于 `<target>` 我顺带确认一下边界:
> 1. **TA 属于哪类?** 主动公开自我表达的公众人物(出书/公职/大量受访)= `public-figure`;有点公开足迹但非主动公众人物 = `semi-public`;普通私人(你的朋友/同事/家人) = `private-individual`;已故 = `deceased`。拿不准我就**就低判**更严的一类。
> 2. 如果是 `semi-public` / `private-individual`:**请一行确认你有授权或正当理由**(本人授权 / 知情同意的关系与用途 / 仅用你合法持有的一手材料自用)。没有的话,私人个体我**不蒸馏**,半公众我**只做 advisor**。
> 3. 如果是 `deceased`:我会在诚实边界写一条 **dignity note**;若 TA 生前是私人个体,还需在世权利人的同意。

判定后立即落变量(供后续阶段读取,**不要硬编码"变成那个人"**):

```yaml
# Phase 0A 产出(写入目标 frontmatter,单一真相源)
target_class:   public-figure | semi-public | private-individual | deceased
consent_basis:  <一行> | N/A
use_case:       roleplay | advisor | decision-reference   # 被 §3 翻转后以翻转值为准
```

### Phase 0A 伦理路由速查

```
判 target_class
├─ public-figure ───────────────→ 无 consent 闸;use_case 用户自选
├─ semi-public ─────────────────→ consent 闸:有? ─是→ 可解锁 roleplay(需显式要求)
│                                            └─否→ 强制 advisor(consent_basis 标"限 advisor 自用")
├─ private-individual ──────────→ consent 闸:有? ─是→ 默认 advisor;显式要求才 roleplay
│                                            └─否→ 拒绝(不建目录)
└─ deceased ────────────────────→ 强制 dignity note;生前 private 量级 → 叠加 consent 闸(权利人)
```

---

_本文件为 distill-forge 的伦理/consent 路由(优化项 #7)。与 SKILL.md 的 Phase 0A、Phase 3 模板选择、frontmatter 约定及「打包发布」清单联动:`consent_basis` 非空、`target_class` 已填,是发布前清单的硬项。_
