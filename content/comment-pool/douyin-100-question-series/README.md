# 碳硅道统 · 抖音100条链式质询评论集

## 定位

红蓝对抗链式质询库，用于抖音评论投放。对应官方定义 v1 **§9「100 质询」**：[官方定义正本](../../../dola-carbon-silicon-framework/docs/official-definition/carbon-silicon-doctrine-official-definition-v1.md)。

## 序号说明（与 `100.pdf` 一致）

| 层级 | 含义 | 示例 |
|------|------|------|
| **评论序号** | 共 100 条抖音评论，PDF/主文档行首单独一行数字 | `1` … `100` |
| **链式子句** | 每条评论内固定 **7 句**，编号 **0.–6.**（不是第 0–6 条评论） | `0. …` 至 `6. …` |
| **items/** | `q-001.md` = 第 **1** 条评论全文；`q-100.md` = 第 **100** 条 | 非 700 个单句文件 |

主文档在每条评论之间留空行，避免评论序号 `2` 紧接在上一条 `6.` 之后被误读。

## 目录

| 文件 | 说明 |
|------|------|
| [`carbon-silicon-100-questions-douyin.md`](carbon-silicon-100-questions-douyin.md) | 100 条完整原文（评论序号 + 前缀 + 0–6 七句） |
| [`manifest.json`](manifest.json) | 元数据与主文档 SHA256 |
| [`items/`](items/) | 单条拆分 `q-001.md` … `q-100.md`（与评论序号一一对应） |

## 标签

`carbon-silicon-doctrine`, `comment`, `red-blue-challenge`, `douyin`

## 校验

- 采样标识：`20260917-douyin-100-question-series-carbon-silicon`
- 主文档 SHA256：`5dac582726eaa018739094e9b15a620f0ace3d9a4728c7ada791c87c73d29c10`

## 分支管控

素材已提交本地分支；远端只读冻结，无明确推送指令不得同步远程。
