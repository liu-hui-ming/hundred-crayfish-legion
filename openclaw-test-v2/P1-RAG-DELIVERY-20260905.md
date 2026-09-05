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

## 3. 文档命中验证（历史探针 + 索引后状态）

| 查询 | 期望文档 | 结果 |
|------|----------|------|
| `0⁰=1=∞=0 本源公理` | `Ch1_本源公理.md` | ✅ score 1.000 |
| `Why Are We V1.0` | `Why-Are-We-V1.0.md` | ✅ 语料已索引（spinoff-debate-papers） |
| `zero power axiom` | `00-zero-power-axiom-V1.0.md` | ✅ 语料已索引 |
| `100 open inquiries` | `100-open-inquiries.md` | ✅ 语料已索引 |
| `Lin Qingxiang 10 questions` | `10-questions.md` | ✅ 语料已索引 |

早期探针日志：`logs/memory-search-rag.log`  
`memory index --force` 成功：`logs/memory-index-force-2026-09-05T12-02-17.log`（426 files indexed）

---

## 4. weixin 插件 hotfix

| 版本 | 状态 |
|------|------|
| 2.1.1（旧拷贝） | ❌ SDK 路径废弃 |
| **2.4.8**（`plugins install`） | ✅ **runtime status: loaded** |

Gateway 探活：`logs/gateway-probe-20260905.log`

---

## 5. 待补（凭证/运行时）

- session 断点续跑 E2E 验收日志（session store 已有 3 entries）
- approval pending 流触发实测（基线 policy 已 `approvals get` 归档）
- Gateway 需保持运行：`start-v2test-gateway.ps1`
