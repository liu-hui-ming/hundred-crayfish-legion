# XIAN 一日一发 · 归档执行硬性要求

**生效日期：** 2026-09-08（修订）  
**适用范围：** `hundred-crayfish-legion` 仓库内全部 XIAN 日报归档与台账联动

---

## 硬性要求（五条）

### 1. 正文正本禁止原地修改

正文**原始正本文件禁止直接修改迭代**。已定稿写入归档路径的 `title.txt` / `body.md` **不得改正文**。

**更新版本**须**新建独立文件夹**存放（例：`docs/issue-exports/xian-daily-2026-09-08/`），禁止覆盖旧文件夹内正本。

### 2. 一组归档 = 一个 commit

每一组 XIAN 归档任务必须生成**单独 commit**，提交备注须含 Issue 号、归档日期、稿件路径。

**禁止**将 XIAN 归档与无关业务改动（RAG、OpenClaw 测试、媒体台账等）**合并进同一 commit**。

**示例：**

```
docs(xian): archive daily #117 2026-09-08 + registry sync
```

### 3. 路径固定 · 生产禁写

| 类型 | 固定路径 |
| --- | --- |
| 归档文件夹 | `docs/issue-exports/xian-daily-YYYY-MM-DD/`（含 `title.txt`、`body.md`） |
| 发布脚本 | `scripts/publish_xian_daily_issue_YYYY_MM_DD.ps1` |
| 台账 | `docs/issue-registry/` |
| 索引 / 变更 | `CHANGELOG.md`、相关 `REGISTRY_XIAN_DAILY_*` 段落 |

**禁止**随意变更目录层级。  
**生产实例、生产目录**（含 `~\.openclaw`、生产 Gateway 工作区）**严禁写入**测试草稿或归档素材；归档仅在本仓 `docs/issue-exports/` 完成。

### 4. 台账 · 索引 · 快照同步闭环

归档完成后必须同步更新：

- **台账：** `docs/issue-registry/`（含 `2026-04-24-p1-p2-axium.md`、`2026-08-15-dt188-closure-issues-ledger.md`）
- **索引：** `CHANGELOG.md`、Issue registry 中 `REGISTRY_XIAN_DAILY_YYYY_MM_DD` 段落
- **快照：** 发布脚本路径、Issue URL、稿件路径在 registry 中可反查

**不允许**「Issue 已发 / 文件已写但台账未登记」。  
涉及 **#79** 等回执依赖时，正文或 Issue 须有明确回执标记；**无回执不得标 POSTED / CLOSED**。

### 5. 链接必须真实

所有对外引用链接（GitHub Issue URL、媒体原文、Wayback 等）必须使用**真实产出链接**。  
**禁止**虚构或占位 URL（如未发布稿件写假 `mp.weixin.qq.com` / `zhihu.com/p/…` 链接）。

---

## 单条归档 SOP（执行顺序）

1. 新建文件夹 `docs/issue-exports/xian-daily-YYYY-MM-DD/`，写入 `title.txt` + `body.md`（定稿后正文不改）
2. 新建 `scripts/publish_xian_daily_issue_YYYY_MM_DD.ps1`
3. 发布 GitHub Issue，记录**真实** Issue URL
4. 更新 `issue-registry` + `CHANGELOG.md` + registry 索引段落
5. 有 #79 等回执依赖时，先对账再改台账状态
6. **单独** `git commit`（仅含本条 XIAN 归档相关文件）

---

## 历史 flat 文件说明

2026-09-07 前部分条目为 flat 文件（`xian-daily-YYYY-MM-DD-body.md` 等于 repo 根下 `docs/issue-exports/`）。**自 2026-09-08 起**，新版本与新版迭代统一采用**独立文件夹**；历史 flat 文件视为已封存正本，**禁止覆盖**，迭代须新建文件夹。
