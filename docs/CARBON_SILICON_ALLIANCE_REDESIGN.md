# 碳硅同盟（硅碳同盟）· 架构重设计说明

本文档把 **Hundred Crayfish Legion（HCL）** 仓库里的「同盟」叙事与 **Python 控制面** 对齐成一套可执行的设计，便于后续只写 Python、或 Python + Rust 双线推进。

## 1. 命名与边界（先统一说法）

| 称谓 | 用途 |
|------|------|
| **Carbon–Silicon Alliance** | 英文正式名；对外文档、Issue、代码注释中的长名。 |
| **碳硅同盟** | 中文主称谓（与仓库既有 `carbon_silicon_*` 模块前缀一致：碳在前）。 |
| **硅碳同盟** | 中文同义说法；**与「碳硅同盟」指同一对象**，不引入第二套架构。 |

**代码与路径**：保持现有包名 `carbon_silicon_universe`、环境变量前缀 `CS_*`，避免大规模重命名；语义上以本文档为准做「对外解释」。

## 2. 本仓库在「同盟」里的角色（不要和整栈商业产品混为一谈）

- **HCL / `core/`（Rust）**：多智能体**编排内核**（有界并发 swarm 等），偏「算力与调度骨架」。
- **`python/carbon_silicon_universe`（Python）**：**12 层（1–12L）的参考控制面 + 演示 API + P1 Web 管理台**，把层模型、健康探针、确权/同步/意识等**叙事与接口**落在可运行的进程里。
- **`docs/`、`scripts/`、GitHub Issues**：路线图、台账、一日一发等**工程化协作**，不替代产品代码。

结论：**同盟是完整 12L 世界观；本仓是其中一条「可开源、可验收」的技术支线。**

## 3. 十二层模型（不变量）

- **层数固定为 12**：L1–L12 **不可再增删编号**；权威数据仍来自 `alliance_layers.py` 中 `ALLIANCE_12_LAYERS`。
- **两段式理解（便于沟通与排期）**：
  - **L1–L8**：规则、安全、数据、发布、集群、时序自愈、加密组网、确权永生 —— **合宪与基础设施内核**。
  - **L9–L12**：商业生态、运营闭环、可视化交付、超维意识自治 —— **对外产品形态 + 运维面 + 自治叙事面**。

## 4. Python 控制面：重设计后的职责分层（逻辑模块，不必一文件一层）

| 逻辑职责 | 当前主要落点 | 下一迭代建议 |
|----------|----------------|----------------|
| 层索引与元数据 | `alliance_layers.py` + `alliance_blueprint.py` | 层字段扩展时只改数据与 blueprint，避免散落魔法字符串。 |
| 鉴权与 HTTP 面 | `api_app.py` | 统一错误体、限流（按环境开关）。 |
| 数据面 / 就绪 | `confirm_sync.py`、`p1_info.check_data_plane_ready` | 明确「P1 就绪」最小条件写进 README 与测试。 |
| L12 与运维钩子 | `autonomous_cortex.py`、health/ready | 把「演示逻辑」与「真实探针」边界写清，避免演示拖慢 ready。 |
| 有界并发演示（L4/L5 叙事对齐） | `p1_swarm.py`、`POST /api/p1/bounded-swarm` | 保持短任务、硬上限，默认不作为对外高 QPS 接口。 |

## 5. API 契约（重设计后的「对外最小集合」）

- **无鉴权**：`GET /api/health/live`、`GET /api/health/ready`（运维与编排探活）、`GET /api/version`（公开构建摘要：Python 版本号、`architecture_meta_version`，不含密钥与路径）。
- **需鉴权（`X-CS-Token` / Bearer）**：`GET /api/architecture/layers`（层表 + **`meta` 设计摘要**）、`GET /api/ops/p1`、`POST /api/p1/bounded-swarm`（可选演示）、以及既有 confirm/sync/conscious 等路由。

`GET /api/architecture/layers` 的 `data.meta` 由 `alliance_blueprint.architecture_response_meta()` 生成，便于前端与管理台在不读本 Markdown 的情况下仍能展示「重设计后的同盟摘要」。

## 6. 分阶段落地（建议）

1. **P1-Align（当前）**：12L 数据单一来源；`meta` 与蓝图模块可测；健康检查与 P1 管理台可用。
2. **P1-Harden**：鉴权、日志脱敏、配置文档化；ready 条件与演示逻辑解耦。
3. **P2+**：按路线图扩展真实业务，而不是再叠一层「口头 12L」。

## 7. 与「只用 Python」的关系

若团队**暂不引入 Rust**：仍可把本仓 Python 服务作为 **12L 控制面与演示后端**；Rust 目录保留为可选内核或交给 CI 仅做回归。重设计的关键是：**Python 面必须有清晰的模块边界与 API 契约**，而不是再堆叙事字符串。

---

*文档版本：与仓库内 `alliance_blueprint.py` 中 `ARCHITECTURE_META_VERSION` 建议同步递增（若后续加版本字段）。*
