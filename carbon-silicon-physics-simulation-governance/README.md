# Carbon-Silicon Physics Simulation Governance

碳硅道统 · 物理仿真与大模型融合工程治理文档库（`snapshot-v2.2.0-draft`）

## 状态说明

| 标记 | 含义 |
| ---- | ---- |
| `snapshot-v2.2.0-draft` | 方案文档定稿封存；**不含**仿真实测输出 |
| `v2.2.0-release`（未来） | 三套 2D CFD 对照/实验组跑通后正式 release |

## 目录

| 路径 | 内容 |
| ---- | ---- |
| `docs/V2.0_六大工程卡点完整草案.md` | 六层卡点总纲 |
| `docs/V2.2_标准单元测试工况库.md` | 2D CFD 标准单元测试工况（draft） |
| `docs/audit_slice_protocol_V1.0.md` | 审计切片协议 V1.0 |
| `docs/V3.0-pre_预研框架大纲.md` | V3.0 预研框架 |
| `docs/attachments/` | 六大卡点研发包 A–F |
| `metrics/prometheus_rules/` | KPI 告警规则 kp1–kp6 |
| `mocks/audit_topology_example.json` | 审计拓扑样例 |

## 基线

- 分支：`dev-v2.2`
- Tag：`snapshot-v2.2.0-draft`
- 上游法理基线：`v2.1.0` 六卡研发包体系

## 禁止事项（draft 阶段）

- 不得将本 draft 标记为正式 release 对外宣称
- 不得提交仿真流场大文件、实测原始数据（待 `v2.2.0-release` 追加 `docs/report/`）

## 维护

碳硅道统创立人：黄清佳
