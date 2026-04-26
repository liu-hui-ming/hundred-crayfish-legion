# GitHub issue draft — P1 only (separate from P2)

**Suggested title (EN):**  
`[P1-Roadmap] HCL: P1 foundation baseline — kernel, service, P1 web, health, deploy, CI`

**Labels (suggested):** `P1-Roadmap`, `documentation`, `enhancement` (as your policy allows)

---

## Body (EN — first post)

**Hundred Crayfish Legion** documents its **P1 (foundation) baseline** on:  
[`https://github.com/liu-hui-ming/hundred-crayfish-legion`](https://github.com/liu-hui-ming/hundred-crayfish-legion)

P1 = **verifiable, shippable minimum**: kernel, API surface, a minimal web console, deploy, health, basic autonomy hook — aligned with the **12L** model in the README. *(Commercial/ops lines L9–L11 in the 12L table are narrative/roadmap; P1 is not a full product bundle.)*

### In repo today (P1 scope)

| Area | What |
|------|------|
| **Rust** | `core/`: `CrayfishSwarm` (bounded parallel), `cargo run --example swarm_tokio --` |
| **Service** | `python -m carbon_silicon_universe` — 12L metadata, L8 attestation + sync, L12 cortex, Flask routes |
| **P1 web** | `GET /` → `/p1/` (static console; `X-CS-Token` must match `CS_UNIVERSE_API_TOKEN`) |
| **Deploy** | `Dockerfile`, `docker-compose.yml` |
| **Ops** | `GET /api/health/live`, `GET /api/health/ready` (sets L12 `SYSTEM_HEALTH_STATUS` on ready) |
| **P1 meta** | `GET /api/ops/p1` (authenticated) |
| **CI** | `.github/workflows/ci.yml` (Python tests + Rust) |
| **Scripts** | `scripts/healthcheck.*` |

**Tests (local):** from `python/`: `python -m unittest discover -s tests`

**SSOT clone:**

```text
https://github.com/liu-hui-ming/hundred-crayfish-legion.git
```

`README` → **P1 基座** table. Issue conventions: `[Announcement]`, `[Manifesto]`, `[P1-Roadmap]`.

---

## 中文（发 Issue 后作首条或次条评论）

**P1 基座（可验收）** 以仓库 `README` 中 **P1 基座** 表为口径：Rust 核、同盟 Python 服务、P1 管理台 `/p1/`、liveness/ready 与 P1 元信息 API、Docker/Compose、CI 与健康脚本；**生产环境请更换** `CS_UNIVERSE_API_TOKEN` 等默认。  
P2 弹性、彩蛋、Axium 升维清单**不在本条**，见**单独**发的 **P2 议题**。

**备案：** 发布后把 Issue 链接与日期记入账务/台账即可。

---

## After publish (台账)

| Field | |
|--------|--|
| Issue URL | *paste* |
| Scope | P1 only |
