# CONTRIBUTING

## 范围

本目录仅归档**文本类**工程治理文档、Prometheus 规则与 JSON 样例。

## 禁止提交

- CFD/仿真输出（VTK、CSV 大流场、checkpoint）
- 未脱敏生产数据
- 覆盖已推送 tag 对应的历史 commit

## 提交流程

1. 在 `dev-v2.2` 分支修改
2. 更新 `CHANGELOG.md`
3. Draft 阶段使用 `snapshot-v2.2.x-draft` tag；实测通过后使用 `v2.2.0-release`
