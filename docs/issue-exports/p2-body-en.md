**P2** in **HCL** = **optional, non-blocking** to mainline releases. Work when capacity allows: short easter-egg check + a **skeleton** checklist for **Axium** / dimensional-uplift handoff.

Repo: [`https://github.com/liu-hui-ming/hundred-crayfish-legion`](https://github.com/liu-hui-ming/hundred-crayfish-legion)

### 1) Easter-egg (short validation)

- **Env (must be set in the process that runs the server):** `HCL_P2_EASTER=1` (or `true` / `yes`)  
- **When on:** `GET /api/p2/easter-egg` → JSON  
- **When off:** `404` (intentional; not discoverable)  
- **No** long-run or large-scale load here.  
- `GET /api/health/live` includes **`hcl_p2_easter: true/false`** so you can see if the process picked up the flag. **Restart** the app after changing env; same terminal as the server, or a new process with the variable set.

### 2) Axium uplift — deferred theme (prep only)

- **File:** `docs/AXIUM_UPLIFT_PREREQUISITES.md` — a **table skeleton**; rows are to be **filled in meetings** with Axium / your programme. It does **not** block publishing P1.  
- Real **Axium** cutover stays on the **programme** calendar, not a single HCL issue.

P1 **foundation** baseline is a **separate** issue: see the **P1-only** thread in this repo (link it in a comment on both sides if helpful).

**Clone**

```text
https://github.com/liu-hui-ming/hundred-crayfish-legion.git
```

`README` → **P2 弹性**; Issue prefixes per `README` (e.g. `[P1-Roadmap]`).

*Draft source: `docs/github-issue-p2-elastic-2026-04-24.md` in repo.*
