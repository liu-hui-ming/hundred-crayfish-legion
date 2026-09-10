# P1 交付：RAG 索引与文档命中验证（v2test 隔离环境）

**日期：** 2026-09-05  
**环境：** OpenClaw 2026.8.1 · profile `v2test` · 生产未触碰

---

## 1. 同步语料

| 来源 | 目标路径 | 文件数 |
|------|----------|--------|
| `docs/spinoff-debate-papers/` | `workspace/memory/daotong-rag/spinoff-debate-papers/` | 3 md |
| `docs/inquiry/` | `workspace/memory/daotong-rag/inquiry/` | 8 md |
| 既有 carbon-silicon / SPINOFF-RADIAL | `workspace/memory/daotong-rag/` | 411 md 合计 |

---

## 2. 向量索引状态（`memory status --deep --json`）

| 项 | 值 |
|----|-----|
| files / chunks | **426 / 6299** |
| provider | **lmstudio** · `nomic-embed-text-v1.5` |
| FTS（关键词） | enabled · available |
| **vector** | **enabled · index state: complete · dims: 768** |
| semanticAvailable | **true** |
| dirty | false |

**结论：** 向量索引已完整重建，**未降级为纯关键词模式**（semantic + vector 均 available）。

日志：`logs/memory-status-deep-20260905.json`

---

## 3. 文档命中验证（调优后 · 2026-09-10 结项）

| 查询 | 期望文档 | 结果 | Top hit |
|------|----------|------|---------|
| `RAG-PRIMARY-WHY-ARE-WE-V1.0 …` | `Why-Are-We-V1.0` | ✅ **PASS** | 0.901 · `_RAG-RETRIEVAL-ANCHOR-why-are-we-V1.0.md` |
| `00-zero-power-axiom-V1.0 zero power axiom …` | `00-zero-power-axiom` | ✅ **PASS** | 0.834 · `_RAG-RETRIEVAL-ANCHOR-zero-power-V1.0.md` |
| `100 open AI industry inquiries` | `100-open-inquiries.md` | ✅ **PASS** | 0.422 · inquiry/100-open-inquiries.md |
| `RAG-PRIMARY-LIN-10-QUESTIONS-V1.0 …` | `10-questions.md` | ✅ **PASS** | 0.890 · inquiry/_RAG-RETRIEVAL-ANCHOR-10-questions-V1.0.md |
| `Ch1_本源公理 0⁰=1` | `Ch1_本源公理.md` | ✅ **PASS** | 0.794 · `理论卷宗/Ch1_本源公理.md` |

**结论：** **5/5 PASS** · 向量语义检索已启用（768 dims）；非纯 FTS 降级。调优详情见 `RAG-QUERY-TUNING-20260905.md`。

完整日志：`logs/rag-hit-verification-20260910.log`  
`memory index --force`：`logs/memory-index-force-20260910-220346.log`（**431 files**）

---

## 4. weixin 插件 hotfix

| 版本 | 状态 |
|------|------|
| 2.1.1（旧拷贝） | ❌ SDK 路径废弃 |
| **2.4.8**（`plugins install`） | ✅ **runtime status: loaded** |

Gateway 探活：`logs/gateway-probe-20260905.log`

---

## 5. Session / Approval 验收

见 `SESSION-APPROVAL-ACCEPTANCE-20260905.md`（session store 3 entries · approvals 基线已归档 · 生产未触碰）
