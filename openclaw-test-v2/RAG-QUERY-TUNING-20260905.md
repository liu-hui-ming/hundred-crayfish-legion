# RAG 查询调优结项（v2test · 2026-09-05）

**环境：** OpenClaw 2026.8.1 · profile `v2test` · 生产未触碰

---

## 调优措施

| 项 | 动作 |
| --- | --- |
| 检索锚点 | 新增/同步 `_RAG-RETRIEVAL-ANCHOR-Ch1-V1.0.md`、`_RAG-RETRIEVAL-ANCHOR-why-are-we-V1.0.md`；既有 zero-power / 10-questions 锚点已入 workspace |
| 查询语句 | `run_rag_hit_verification.ps1` 改用 `RAG-PRIMARY-*` 检索 token；zero-power 改用 ASCII 安全查询 + `alt=zero-power` 匹配 |
| CLI 路径 | 脚本改为 `node.exe` 直调 `openclaw.mjs`，规避 `openclaw.cmd` CLR 异常 |
| 索引 | `memory index --force` 重建完成：**431 files**（含 Ch1 / Why-Are-We / zero-power 锚点） |

---

## 命中验证（`logs/rag-hit-verification-20260910.log` · 结项）

| 查询 | 期望 | 调优前 | 调优后（2026-09-10） |
| --- | --- | --- | --- |
| `RAG-PRIMARY-WHY-ARE-WE-V1.0 …` | `Why-Are-We-V1.0` | PARTIAL (README) | ✅ PASS（0.901） |
| `00-zero-power-axiom-V1.0 zero power axiom …` | `00-zero-power-axiom` | PARTIAL (README) | ✅ PASS（0.834 · 锚点） |
| `100 open AI industry inquiries` | `100-open-inquiries` | PASS | ✅ PASS（0.422） |
| `RAG-PRIMARY-LIN-10-QUESTIONS-V1.0 …` | `10-questions` | PARTIAL (README) | ✅ PASS（0.890） |
| `Ch1_本源公理 0⁰=1` | `Ch1_本源公理` | PARTIAL (典藏卷别名) | ✅ PASS（0.794） |

**模式确认：** 向量索引 complete · semanticAvailable true · **未降级纯 FTS**（见 `P1-RAG-DELIVERY-20260905.md` §2）。

**结项：** 5/5 PASS · `memory index --force` 431 files · 日志 `memory-index-force-20260910-220346.log`。
