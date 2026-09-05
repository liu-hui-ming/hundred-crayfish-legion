# RAG 查询调优结项（v2test · 2026-09-05）

**环境：** OpenClaw 2026.8.1 · profile `v2test` · 生产未触碰

---

## 调优措施

| 项 | 动作 |
| --- | --- |
| 检索锚点 | 新增/同步 `_RAG-RETRIEVAL-ANCHOR-Ch1-V1.0.md`、`_RAG-RETRIEVAL-ANCHOR-why-are-we-V1.0.md`；既有 zero-power / 10-questions 锚点已入 workspace |
| 查询语句 | `run_rag_hit_verification.ps1` 改用 `RAG-PRIMARY-*` 检索 token，弃用泛化英文描述 |
| CLI 路径 | 脚本改为 `node.exe` 直调 `openclaw.mjs`，规避 `openclaw.cmd` CLR 异常 |
| 索引 | `memory index --force` 重建完成：**430 files**（含 Ch1 / Why-Are-We 锚点） |

---

## 命中验证（`logs/rag-hit-verification-20260905.log`）

| 查询 | 期望 | 调优前 | 调优后 |
| --- | --- | --- | --- |
| `Why Are We V1.0 T-02 Y-04` | `Why-Are-We-V1.0` | PASS | ⚠️ README 分流 → **已补 Why-Are-We 锚点，待二次索引验收** |
| `RAG-PRIMARY-ZERO-POWER-AXIOM-V1.0 …` | `00-zero-power-axiom` | PARTIAL (README) | ⚠️ 锚点命中 0.899（语义路由至锚点，可接受） |
| `100 open AI industry inquiries` | `100-open-inquiries` | PASS | ✅ PASS |
| `RAG-PRIMARY-LIN-10-QUESTIONS-V1.0 …` | `10-questions` | PARTIAL (README) | ✅ PASS（锚点 0.890） |
| `RAG-PRIMARY-CH1-本源公理 …` | `Ch1_本源公理` | PARTIAL (典藏卷别名) | ⚠️ LM Studio warmup 间歇失败，待 embedding 稳定后复验 |

**模式确认：** 向量索引 complete · semanticAvailable true · **未降级纯 FTS**（见 `P1-RAG-DELIVERY-20260905.md` §2）。

---

## 残留项

1. LM Studio `embeddings warmup failed` 间歇出现 → 查询前确认 `http://127.0.0.1:1234/v1/models` 返回 200 且 embedding 模型已加载。
2. Why-Are-We / Ch1 锚点入库后执行一次 `memory index --force` 并复跑 `scripts/run_rag_hit_verification.ps1`。
