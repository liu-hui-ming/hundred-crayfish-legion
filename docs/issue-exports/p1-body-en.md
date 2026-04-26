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

*Draft source: `docs/github-issue-p1-baseline-2026-04-24.md` in repo.*
