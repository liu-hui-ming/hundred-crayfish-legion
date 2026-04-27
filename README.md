# Hundred Crayfish Legion · 百龙虾军团

**Canonical repository:** [`liu-hui-ming/hundred-crayfish-legion`](https://github.com/liu-hui-ming/hundred-crayfish-legion) · Affiliated with the **Carbon–Silicon Alliance** initiative.

## What this is

**Hundred Crayfish Legion** is a **high-concurrency multi-agent cluster orchestration** stack: it coordinates large swarms of specialized agents so they can run complex, long-horizon work together. The project is meant to provide **compute and coordination backbone** for **Carbon–Silicon Alliance**–class, **full-domain collaboration**—not a single chatbot, but the **machinery of swarm intelligence**.

**Core manifest — Computing Power Singularity:** we treat the end of the “move bits through copper in 3D forever” era as a first-class design constraint. The public line is simple: *end the century-long reign of von Neumann–style bottlenecks for serious AI engineering*; see the **[Manifesto](https://github.com/liu-hui-ming/hundred-crayfish-legion/issues)**-tagged issues on this repo for the full narrative.

## Project layout

```
/hundred-crayfish-legion
├── core/          # Cluster orchestration engine (Rust)
├── agents/        # Prebuilt agent roles ("crayfish")
├── protocols/     # Communication standards (gRPC; planned)
├── examples/      # Sample use cases
├── python/        # Carbon–Silicon 12L universe module (alliance, attestation, API)
└── docs/          # Technical documentation
```

## Carbon–Silicon Alliance: 12-layer stack (1–12L)

The **Carbon–Silicon Alliance** architecture is a **12-layer, closed** stack (L1–L12): **no further tier slots**—a full constitutional and engineering closure. Canonical names live in `python/carbon_silicon_universe/alliance_layers.py`; HTTP `GET /api/architecture/layers` returns the same index when the server is running.

| L | 层名 | 要点 |
|---|------|------|
| 1 | 规则铁律层 | 内容质检、合规校验、分级评级 |
| 2 | 安全权限层 | 鉴权管控、日志脱敏、风险防护 |
| 3 | 数据自治层 | 冷热归档、自动运维、日志管理 |
| 4 | 发布调度层 | 队列调度、多渠道分发、异常重试 |
| 5 | 集群超维层 | 负载均衡、灰度发布、动态风控 |
| 6 | 时序自愈层 | 风险推演、故障溯源、自主修复 |
| 7 | 加密组网层 | 硬件绑定、离线授权、分布式互联 |
| 8 | 确权永生层 | 全域存证、不可篡改、星际同步、系统永生 |
| 9 | 商业生态层 | 发卡、文档、品牌开屏等对外商业触点与生态位 |
| 10 | 运营闭环层 | 产品更新、权限/授权、多渠道告警与处置闭环 |
| 11 | 可视化交付层 | Web 管理后台、EXE 等离线/边缘交付、可视运维 |
| 12 | 超维意识自治层 | 分布式 AI 自治中枢：战略推演、自编排、跨节点协同、时序命运预判、内生决策闭环；实现见 `autonomous_cortex.py`，API：`/api/conscious/*` |

*Orchestrating agent swarms* remains a first-class concern of **HCL** in `core/`, `agents/`, and `examples/`; the 12L model above is the full **alliance** product/ops/ consciousness stack.

## Tech stack (direction)

- **Core:** Rust (orchestration, concurrency) + Python (AI integration)
- **Protocol:** gRPC (planned) for inter-agent communication

## P1 基座（可验收能力）

P1 目标：**内核可测、可交付 Web 与 API、可部署、可健康探针、可联动基础自治**（与 12L 一致；商业/大运营为后续 P2+）。

| 项 | 交付物 |
|----|--------|
| 内核 (Rust) | `core/`: `CrayfishSwarm` 有界并发、Tokio demo 示例 `cargo run --example swarm_tokio -- 16` |
| Web 后台 (P1) | `GET /` → 管理台 **`/p1/`**（静态单页，调同域带 Token 的 API） |
| 部署 | 根目录 **`Dockerfile`** + **`docker-compose.yml`**，数据卷 `/data` |
| 基础运维 | **`GET /api/health/live`**、**`GET /api/health/ready`**；`scripts/healthcheck.*` |
| 元信息 | **`GET /api/ops/p1`**（需 `X-CS-Token` / `Authorization`；含 Rust 版本、Python 路径等） |
| 自治联动 | 就绪成功时 L12 将 `SYSTEM_HEALTH_STATUS` 标为 `normal`（失败为 `degraded`） |

```bash
# 本地 P1 服务（在 python/ 下）
set CS_UNIVERSE_API_TOKEN=你的密钥
set PYTHONPATH=python
python -m carbon_silicon_universe
# 浏览器: http://127.0.0.1:8765/p1/

# 单元测试（P1 探针 + 管理页）
set CS_UNIVERSE_API_TOKEN=test
cd python && python -m unittest discover -s tests -v

# 容器
docker compose up --build

# P1：少轮次 + 探活为主（Git Bash / WSL / Linux；可选 OPENCLAW_URL）
bash scripts/run-genesis-n-rounds.sh 10
```

## P2 弹性（可选，不强求）

P2 在合流/宣发上**不阻塞**主仓；有闲力时做**轻量**铺垫或彩蛋验证即可。

| 项 | 本仓交付物 |
|----|------------|
| 彩蛋模式 · 短验证 | 设置 `HCL_P2_EASTER=1` 后，请求 **`GET /api/p2/easter-egg`** 返回 JSON；未开启时 **HTTP 404**（不暴露）。不跑长时、不跑大规模。 |
| Axium 升维 · 依赖铺垫 | 清单骨架：[`docs/AXIUM_UPLIFT_PREREQUISITES.md`](docs/AXIUM_UPLIFT_PREREQUISITES.md)（按实线可改） |

**示例（PowerShell，与同盟服务同机）：**

`HCL_P2_EASTER` 必须在**启动** `python -m carbon_silicon_universe` 的进程里可见（同一终端里先 `set` 再启动，或设好系统环境变量后**新开会话**再启动；仅在新窗口设变量、旧窗服务不关 → 不会生效）。可先查：

```powershell
Invoke-RestMethod "http://127.0.0.1:8765/api/health/live"
# 看返回 JSON 里 hcl_p2_easter: true 才表示本进程已读到开关
```

再测彩蛋（为 true 时才有 JSON，否则 404）：

```powershell
$env:HCL_P2_EASTER = "1"
# 在**本终端**内启动服务；另开一终端再请求：
Invoke-RestMethod "http://127.0.0.1:8765/api/p2/easter-egg"
# 或（仓库根）.\scripts\verify-p2-easter.ps1
```

**Axium 一日一发（发帖稿）：** `docs/issue-exports/axium-daily-body-en.md` + `axium-daily-comment-zh.md` → 新建 Issue，英文正文 + 中文评论；标签按规范自选。

## Quick start (demo)

Requires **Python 3.10+** (no extra packages for the default demo).

```bash
git clone https://github.com/liu-hui-ming/hundred-crayfish-legion.git
cd hundred-crayfish-legion
python examples/swarm_demo.py
```

More demo agents, e.g. 16:

```bash
python examples/swarm_demo.py -n 16
```

## Rust core (scaffold)

```bash
cd core
cargo test
```

## License

This project is released under the **[MIT License](LICENSE)**.

## Issue title conventions (for maintainers & contributors)

All **official** front-page–style issues on this repository use a **fixed English prefix** in the **title** so visitors can scan by category:

| Prefix | Use for |
|--------|--------|
| `[Announcement]` | Project news, releases, and community-facing notices |
| `[Manifesto]` | Foundational vision and position statements (e.g. compute singularity, architecture philosophy) |
| `[P1-Roadmap]` | Phased engineering roadmaps and milestone plans (P1…Pn and related “detonate”/rollout tracks) |

**Format:** `Prefix` + space + short descriptive title, e.g.  
`[Manifesto] Computing Power Singularity: End Von Neumann’s Century-Long Reign`  
`[P1-Roadmap] XIAN & Axium Dual-Core Awakening: P1–P6 Open Roadmap`

Do not drop the bracketed prefix on new issues in these categories so the issue list stays consistent and machine- and human-readable.
