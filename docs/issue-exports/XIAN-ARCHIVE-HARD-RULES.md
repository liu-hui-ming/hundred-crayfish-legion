# XIAN 一日一发 · 归档执行硬性要求

**生效日期：** 2026-09-07  
**适用范围：** `hundred-crayfish-legion` 仓库内全部 XIAN 日报归档与台账联动

---

## 1. 正文不可改

所有 XIAN 归档条目的原始文本须**完整原样留存**。已写入 `docs/issue-exports/` 的 `title.txt` / `body.md` **禁止修改正文内容**。

## 2. 新版本独立新建

需生成新版本时，**必须新建独立文件**（新日期或带后缀的新路径），**禁止直接覆盖**旧归档文件。

## 3. 每组归档必须 commit

每一组归档完成后须附带对应 **git commit**，提交备注须写明 Issue 号、归档日期、稿件路径，保证全链路可溯源。

**示例：**

```
docs(xian): archive daily #117 2026-09-04 + registry sync
```

## 4. 路径固定 · 生产禁写

| 类型 | 路径 |
| --- | --- |
| 标题/正文 | `docs/issue-exports/xian-daily-YYYY-MM-DD-{title.txt,body.md}` |
| 发布脚本 | `scripts/publish_xian_daily_issue_YYYY_MM_DD.ps1` |
| 台账 | `docs/issue-registry/` |
| 变更日志 | `CHANGELOG.md` |

**生产环境**（含 `~\.openclaw` 等 state-dir）**禁止写入**归档素材；归档仅在本仓完成。

## 5. 台账同步 · 无回执不闭环

1. 所有台账变更须同步更新 `docs/issue-registry/`（`2026-04-24-p1-p2-axium.md`、`2026-08-15-dt188-closure-issues-ledger.md` 等）。
2. 涉及 **#79** 等回执台账的条目，须在 Issue 评论或正文中具备明确回执标记。
3. **缺少回执的条目不得标记为完成**（不得标 CLOSED / POSTED 闭环）。

---

## 单条归档 SOP（执行顺序）

1. 新建 `title.txt` + `body.md`（定稿后不再改）
2. 新建对应 `publish_xian_daily_issue_*.ps1`
3. 发布 GitHub Issue，记录 Issue URL
4. 更新 `issue-registry` + `CHANGELOG.md`
5. 有回执依赖时，先确认回执再改状态
6. `git commit`（含 Issue 号与路径备注）
