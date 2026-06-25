# source-gating · 来源 provenance-first 闸门

> 对应优化项 **#8(provenance-first 采集)** 与 **#10(白名单不等于无条件可信)**。
> 服务于最高原则:**标注了局限的诚实 60 分,胜过看起来 90 分的伪造品。**
> 本文件被 **Phase 1(六路并行采集)** 与 **Phase 1.5(评审闸)** 引用;判定结果最终落到 `references/research/quotes.jsonl` 的 `tier` / `file` / `span` 字段。

一句话:**先问素材从哪来、谁写的,再问它说了什么。** host 与作者身份是闸门;内容是否"听起来很对"不是。

---

## 0. 为什么是 provenance-first

蒸馏的死穴是 AI 凭训练记忆"造人格"。防线只有一条:**每条素材都能回溯到一个落盘的、可逐字核验的原文件**。所以:

- 判定顺序固定:**host(域名/平台)→ author(谁署名)→ tier(一手/二手/推测)→ 落盘 → 记账**。
- host 黑名单是**默认拒**而非永久拒——存在"作者自有可验证渠道"的明确例外。
- 白名单媒体**不享受无条件可信**——每篇仍须逐篇判一手/二手。
- 任何"我搜到一个 URL 说他这么想"的断言,在没经 `fetch_source.py` 落盘 + `quality_check.py` 的 span 核验前,**一律不算一手**。

---

## 1. 默认拒名单(host blacklist)

以下 host 默认拒收,理由是高比例的洗稿/搬运/伪原创/不可回溯二次加工,provenance 链天然断裂:

| host | 默认动作 | 典型问题 |
|---|---|---|
| 知乎(zhihu.com) | 默认拒 | 匿名/化名答主、二手转述、无法验证署名 |
| 微信公众号(mp.weixin.qq.com) | 默认拒 | 营销号搬运、标题党、原文常已被洗稿 |
| 百度系(baijiahao / 百度知道 / 百科镜像) | 默认拒 | 聚合/SEO 农场、来源链断裂 |

> 同类延伸(同样默认拒):今日头条号、搜狐号、网易号等"自媒体号"聚合页,以及任何无法定位原始作者的内容农场镜像。

### 1.1 例外:作者自有可验证渠道(author-owned)

当能**可验证作者身份**时,即使 host 在黑名单上,也**接受**该素材,且 `tier` 仍按内容性质判(可为"一手"),但**必须加 note**。可验证身份指满足以下任一:

1. **官方/认证账号且账号名匹配目标**:平台蓝 V / 官方认证,账号主体明确就是目标本人或其官方实体,账号名与目标一致。
2. **目标第一人称署名原创**:正文是目标本人以第一人称署名的原创(非记者转述、非"据其透露"),且能在该认证账号下找到原帖。

满足例外时:

- `tier` 照常判(本人署名原创 → 一手)。
- 在 quotes.jsonl 该条加 `"note":"blacklisted-host-but-author-owned"`。
- **必须在 Phase 1.5 评审闸显式列为"待批"项**,逐条让人点头后才算数(对应 SKILL.md "所有 blacklist 豁免项" 展示)。
- 仍须经 `fetch_source.py` 落盘 + span 可核验。无法落盘核验 → 退回默认拒。

判不准作者身份(化名、转载、"网友整理"、截图无原账号)→ **回到默认拒**,不进豁免。

---

## 2. 白名单不享受无条件可信

36氪 / 晚点LatePost / 财新 / 第一财经 / 界面等优质媒体进白名单,只代表**值得抓**,**不代表整篇都是一手**。每篇仍须逐篇贴标签:

| 内容形态 | tier | 说明 |
|---|---|---|
| 目标本人**署名访谈逐字**(Q&A 原话) | 一手 | 抓目标的原话 span,而非记者的转述句 |
| 目标本人**署名 op-ed / 专栏** | 一手 | 第一人称署名原创 |
| 记者**综述/特稿**(转述目标观点) | 二手 | "据其表示""他认为"=记者笔,不是目标原话 |
| **PR 通稿 / 公关口径 / 软文** | 二手(或丢弃) | 利益相关,口径非目标自发表达 |
| 第三方**评论/分析**目标 | 二手 | 归到 `04-他者.md` |

> 关键操作:**在白名单媒体的访谈里,只把目标括号内/引号内的逐字答话取为一手 span;记者的串场叙述一律二手。** 一篇文章里两种 tier 并存是正常的。

---

## 3. 一手 / 二手 / 推测 判定规则(对齐 quotes.jsonl 的 tier)

判定结果直接写入 `references/research/quotes.jsonl` 的 `tier` 字段,取值 ∈ `一手` | `二手` | `推测`(见 SKILL.md CONTRACT §A)。quotes.jsonl 每行形如:

```json
{"id":"q001","model":"01-著作","tier":"一手","text":"完整引用原文","source":"来源可读名称","file":"sources/2019_interview.txt","span":"必须逐字出现在 file 里的片段","lang":"zh","date":"2019"}
```

### 3.1 判定标准

| tier | 定义 | 必填 | 例子 |
|---|---|---|---|
| `一手` | 目标**本人**的原始表达:署名书/长文、访谈逐字答话、本人社媒原帖、本人演讲逐字 | **`file` + `span` 必填**(span 须逐字出现在落盘文件里) | 自传段落;播客里他亲口说的句子;认证账号原帖 |
| `二手` | **他人转述/综述**目标的观点:记者特稿、PR 通稿、第三方评论、"据传/据透露" | `source` 必填;`file` 建议有 | 36氪综述里"他认为…";同行回忆 |
| `推测` | 无法落盘核验、或经 span 核验失败被降级、或仅凭模型记忆/合理外推 | — | 断言的 URL;span 对不上的引用;AI 补的"他大概会这么想" |

### 3.2 硬性约束(与 CONTRACT 完全一致)

- `tier=="一手"` 时 `file` 与 `span` **必填**。
- `quality_check.py` 会在归一化(去空白/标点差异)后核验 `span` 确在 `references/<file>` 中出现;**对不上 → 该条自动降级为 `推测`**。
- 翻译材料:`lang` 标源语言,`span` 用**源语言**片段(不要用译文回填 span)。
- author-owned 豁免项额外带 `"note":"blacklisted-host-but-author-owned"`。

---

## 4. "一手"的唯一成立路径:落盘 + span 核验

> **断言 URL 不算一手。** 一条素材要拿到 `tier:"一手"`,它必须同时满足两件事,缺一不可:

1. **经 `fetch_source.py` 落盘**:
   ```bash
   python scripts/fetch_source.py <url> --skill <skill_dir>
   ```
   把原文存进 `<skill_dir>/references/sources/`,回传 `{relpath, sha256, bytes}`。`relpath` 即写进 quotes.jsonl 的 `file`。字幕先 `python scripts/srt_clean.py <in.srt>` 清洗再落盘。
2. **经 `quality_check.py` 的 span 核验**:`span` 必须能在落盘文件里逐字(归一化后)定位到。

任一不满足 → 该条**不能是一手**:

- 只有 URL、没落盘 → `推测`。
- 落了盘但 span 对不上 → `quality_check.py` 自动降级为 `推测`。
- 黑名单 host 且作者身份不可验证 → 默认拒,不进库。

Phase 1.5 评审闸正是用 `quality_check.py` 把 **claimed 一手 vs verified 一手** 的差值摊给人看,让造假在合成前暴露。`fame_tier=high` 的一手占比闸门(>70%)算的是 **verified** 一手,不是 claimed。

---

## 5. 决策流程(文字版流程图)

拿到**一条**素材后,按下面顺序走;每个分叉只有"继续 / 退出"两条路:

```
START：拿到一条素材(URL 或本地文件 或一段引用)
  │
  ├─[1] 判 HOST(域名/平台)
  │     ├─ host ∈ 黑名单(知乎/公众号/百度系/自媒体号)？
  │     │     ├─ 是 → 去 [2] 判作者(可能走 author-owned 例外)
  │     │     └─ 否 → host ∈ 白名单或常规可溯源站？→ 去 [3]
  │     │
  ├─[2] 判 AUTHOR(仅黑名单 host 需要;或任何署名存疑时)
  │     ├─ 可验证作者身份？
  │     │   (官方/认证账号且账号名匹配目标  OR  目标第一人称署名原创)
  │     │     ├─ 是 → 接受;打标 note=blacklisted-host-but-author-owned
  │     │     │        → 标记为"Phase 1.5 待批" → 去 [3]
  │     │     └─ 否 → ✗ 默认拒,丢弃(不进 quotes.jsonl)→ END
  │     └─(白名单 host 无需走例外,直接 [3])
  │
  ├─[3] 判 一手 / 二手 / 推测
  │     ├─ 目标本人原始表达(署名原创 / 访谈逐字 / 本人原帖)？ → 候选「一手」→ 去 [4]
  │     ├─ 他人转述 / 综述 / PR / 第三方评论？               → tier=二手 → 去 [5]
  │     └─ 无法核验 / 仅凭记忆外推？                         → tier=推测 → 去 [5]
  │
  ├─[4] 落盘(仅「一手」候选必须过此关)
  │     ├─ fetch_source.py 落盘到 sources/  → 拿到 file(relpath)+ sha256
  │     ├─ (字幕先 srt_clean.py)
  │     ├─ span 能在落盘文件里逐字定位？
  │     │     ├─ 是 → tier=一手(file+span 齐全)→ 去 [5]
  │     │     └─ 否 → 降级 tier=推测 → 去 [5]
  │     └─ 没法落盘(只有断言 URL) → 降级 tier=推测 → 去 [5]
  │
  └─[5] 记账:写入 references/research/quotes.jsonl 一行
        {id, model:对应六路之一, tier, text, source, file?, span?, lang, date, note?}
        → END
        (Phase 1.5：quality_check.py 复核所有「一手」的 span;
         展示 claimed vs verified 差值 + 所有 author-owned 待批豁免项,人点头)
```

### 5.1 一个端到端示例(author-owned 例外)

> 素材:某 mp.weixin.qq.com 文章,作者为目标本人认证公众号,第一人称署名,讲他对某产品决策的复盘。

1. **[1] host**:`mp.weixin.qq.com` → 黑名单 → 走 [2]。
2. **[2] author**:认证主体=目标本人,账号名匹配,第一人称署名原创 → 满足例外 → 接受 + `note=blacklisted-host-but-author-owned` + 标"Phase 1.5 待批"。
3. **[3] tier**:本人署名原创 → 候选一手。
4. **[4] 落盘**:`fetch_source.py` 存到 `sources/2026_wechat_postmortem.txt`,span 取那段第一人称复盘原话,核验通过 → `tier:"一手"`。
5. **[5] 记账**:
   ```json
   {"id":"q042","model":"01-著作","tier":"一手","text":"……当时我们放弃了 A 方案,因为……","source":"目标本人公众号·产品复盘","file":"sources/2026_wechat_postmortem.txt","span":"当时我们放弃了 A 方案","lang":"zh","date":"2026","note":"blacklisted-host-but-author-owned"}
   ```
6. Phase 1.5:此条出现在豁免待批清单,人确认作者身份无误后才计入 verified 一手占比。

### 5.2 反例(应被拒/降级)

- 知乎匿名答主"整理的马斯克语录" → [1] 黑名单 → [2] 作者不可验证 → **默认拒,丢弃**。
- 36氪特稿里"据他透露,公司将…" → 白名单但属记者转述 → `tier:"二手"`。
- 只贴了一个 URL 声称"他说过 X",未落盘 → `tier:"推测"`(断言 URL 不算一手)。
- 落了盘但 span 在文件里找不到 → `quality_check.py` 自动降级为 `推测`。

---

## 6. 速查

- 默认拒:知乎 / 公众号 / 百度系 / 各家自媒体号。
- 唯一豁免:作者自有可验证渠道 → 接受 + `note=blacklisted-host-but-author-owned` + Phase 1.5 待批。
- 白名单 ≠ 可信:逐篇判,记者笔=二手,本人逐字=一手。
- 一手成立 = 本人原始表达 **且** `fetch_source.py` 落盘 **且** `span` 经 `quality_check.py` 核验。
- 断言 URL、span 对不上、记忆外推 → `推测`。
- 一切判定结果落到 `references/research/quotes.jsonl` 的 `tier`/`file`/`span`/`note`。
