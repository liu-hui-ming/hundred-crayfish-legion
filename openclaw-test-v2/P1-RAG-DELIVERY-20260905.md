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

## 3. 文档命中验证（`run_rag_hit_verification.ps1` · 2026-09-05）

| 查询 | 期望文档 | 结果 | Top hit |
|------|----------|------|---------|
| `Why Are We V1.0 T-02 Y-04` | `Why-Are-We-V1.0.md` | ✅ **PASS** | 0.434 · spinoff-debate-papers/Why-Are-We-V1.0.md |
| `100 open AI industry inquiries` | `100-open-inquiries.md` | ✅ **PASS** | 0.422 · inquiry/100-open-inquiries.md |
| `zero power axiom manifesto` | `00-zero-power-axiom-V1.0.md` | ⚠️ PARTIAL | 0.705 · spinoff-debate-papers/README.md（邻近索引） |
| `Lin Qingxiang 10 questions` | `10-questions.md` | ⚠️ PARTIAL | 0.691 · inquiry/README.md（邻近索引） |
| `0⁰=1=∞=0 本源公理` | `Ch1_本源公理.md` | ⚠️ PARTIAL | 0.515 · 内核典藏卷/0^0=1创世公理正本.md |

**模式：** 向量语义检索已启用（768 dims）；非纯 FTS 降级。PARTIAL 为语义邻近文档分流，可优化 query 或 README 元数据。

完整日志：`logs/rag-hit-verification-20260905.log`  
`memory index --force`：`logs/memory-index-force-2026-09-05T12-02-17.log`（426 files）

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
