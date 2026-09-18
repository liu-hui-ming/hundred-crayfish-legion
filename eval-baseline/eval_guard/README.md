# eval_guard｜十维觉知标尺最小评估原型

[System_Tag: CANONICAL-v9.2-calibrated]

## 目录归属

工程层独立目录：`eval-baseline/eval_guard`

> 与 CH0–CH5 叙事卷宗严格双仓隔离；工程真值源镜像仓 `carbon-silicon/twelve-meridians` 同路径布局。

## 文件清单

1. `eval_guard.py`：主评估程序（3 维度 × 15 探针框架，规则由 JSON 驱动）
2. `probe_definition.json`：探针、权重、阈值、关键词集合（业务规则在此修改，勿改主程序计分逻辑）
3. `sample_report.md`：Markdown 评估报告样例 / 运行输出目标

## 运行方式

```bash
cd eval-baseline/eval_guard
python eval_guard.py
```

## 输入输出规范

| 项 | 说明 |
| --- | --- |
| 输入 | `evaluate(model_input, model_output)` 两段文本；主程序示例为占位字符串 |
| 配置 | 同目录 `probe_definition.json` |
| 输出 | 终端 JSON 摘要 + `sample_report.md`（各维度分、探针明细、输入/输出 SHA256） |

## 运维约束（归档）

1. 运维仅负责归档、哈希校验、维护 `CH0-Canonical-Charter/manifest.json`；禁止擅自修改打分与探针执行逻辑（`eval_guard.py`）。
2. 全部文件编码 UTF-8 无 BOM。
3. 探针业务填充仅更新 `probe_definition.json`，再重算 SHA256、更新 manifest。
4. 未经指令禁止 push 远端 `main`；本仓工程层归档随 `dev-v2.2` 镜像推送策略执行。

## 层属性

- **layer**: `engineering-layer`（见全局 manifest → `eval_baseline_batches`）
