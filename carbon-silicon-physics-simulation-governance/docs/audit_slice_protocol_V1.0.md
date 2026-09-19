---
document_id: GOV-AUDIT-SLICE-PROTOCOL
version: V1.0
---

# Audit Slice Protocol V1.0

## 1. 目的

为物理仿真 + AI 融合 pipeline 提供**可复现、可哈希、可切片**的审计轨迹，支撑 kp6 时序漂移检测。

## 2. 切片定义

| 字段 | 类型 | 说明 |
| ---- | ---- | ---- |
| `slice_id` | string | UUID |
| `run_id` | string | 单次 pipeline 运行 ID |
| `timestamp` | ISO8601 | UTC |
| `stage` | enum | `ingest` / `mesh` / `solve` / `ai_infer` / `merge` / `export` |
| `topology_ref` | string | 拓扑节点 ID（见 mocks） |
| `input_hash` | sha256 | 输入 artifact 哈希 |
| `output_hash` | sha256 | 输出 artifact 哈希 |
| `kpi_snapshot` | object | kp1–kp6 即时值 |
| `prev_slice_id` | string | 上一切片 ID（链式） |

## 3. 哈希规则

1. 规范化 JSON（键排序、UTF-8、无多余空白）后 SHA256
2. 浮点保留 6 位小数再哈希
3. 禁止在哈希计算前写入 `output_hash` 字段本身

## 4. 切片链

```
slice[0].prev_slice_id = null
slice[n].prev_slice_id = slice[n-1].slice_id
```

## 5. 告警联动

- kp6_audit_temporal_drift：相邻切片 KPI 向量 L2 距离超阈触发
- 与 Prometheus `metrics/prometheus_rules/kp6_audit_temporal_drift.yml` 对齐

## 6. 存储建议

- Draft：JSON Lines 本地文件
- Release：对象存储 + 不可变索引
