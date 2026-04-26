**发布为正式 Issues：** 与 P1 同用 `scripts/publish_p1_p2_github_issues.ps1` 一次建两条；或从 `docs/issue-exports/p2-body-en.md` + `p2-comment-zh.md` 手建 [New issue](https://github.com/liu-hui-ming/hundred-crayfish-legion/issues/new)。

---

# GitHub issue draft — P2 only (separate from P1)

**Suggested title (EN):**  
`[P1-Roadmap] HCL: P2 elastic — easter-egg (short check) + Axium uplift prerequisite list`

**Labels (suggested):** `P1-Roadmap` or a lighter `enhancement` / `documentation` per policy

---

## Body (EN — first post)

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

P1 **foundation** baseline is a **separate** issue: see the **P1-only** thread on this repo (same day / linked manually).

**Clone**

```text
https://github.com/liu-hui-ming/hundred-crayfish-legion.git
```

`README` → **P2 弹性**; Issue prefixes per `README` (e.g. `[P1-Roadmap]`).

---

## 中文（评论用）

- **P2 弹性、不强求**：不阻塞主仓/主发；彩蛋仅短验，`HCL_P2_EASTER` 须在**启动服务**的同一进程环境里生效。  
- **Axium 顺延/升维主题**：`docs/AXIUM_UPLIFT_PREREQUISITES.md` 为**依赖表骨架**，**待与 Axium 会签填行**；真升维以项目日程为准。  
- **P1 基座** 请见**另条** P1 单独议题，**勿与本条混发为一条长帖**时若你方更习惯，也可在两条之间互相在评论里**互链**。

**备案：** Issue 链接 + 日期。

---

## After publish (台账)

| Field | |
|--------|--|
| Issue URL | *paste* |
| Scope | P2 only (easter + Axium prep) |
