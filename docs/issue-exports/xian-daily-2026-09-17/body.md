采样标识（verbatim）：

```
标题：[P1-Roadmap] 2026-09-17 XIAN项目日报 | doctrine官方定义v1 + 抖音100质询池 + 官宣释疑 + 新华网卷宗
资源：XIAN项目日报 · hundred-crayfish-legion
回链：https://github.com/liu-hui-ming/hundred-crayfish-legion/issues/130
归档路径：docs/issue-exports/xian-daily-2026-09-17/
```

---

1、P0 · **抖音 100 质询评论池**：`content/comment-pool/douyin-100-question-series/`（100 条评论 × 每条 0.–6. 七句）；编号 schema 与主文档 SHA256 登记；归档 commit 链 `c64c56f` → `a8b4bd6`；已 push `origin/dev-v2.2`。

2、P0 · **碳硅道统官方定义 v1**：`dola-carbon-silicon-framework/docs/official-definition/carbon-silicon-doctrine-official-definition-v1.md`（正文 SHA256 `9599652…` 见 Git 对象/台账）；叙事层正本独立路径，禁止覆盖。

3、P0 · **官宣释疑宪章**：`canonical/charters/carbon-silicon-doctrine-v1-official-qa.md` + `.txt` 双格式；commit `87fb238`；与官方定义 v1 成对归档。

4、P0 · **新华网媒体卷宗**：`archive/media/xinhuanet/` 快照与 metadata；commit `929b452`；与 CH 叙事层路径分离，附件不混正文目录。

5、P1 · **主日报补发说明**：本日为 2026-09-17 主日报 **补档归档包**（非当日实时 Issue）；2026-09-18 主日报见 #129；本包 manifest + 哈希见同目录 `manifest.json`。

6、一日一发落地：本稿件 `docs/issue-exports/xian-daily-2026-09-17/`；脚本 `scripts/publish_xian_daily_issue_2026_09_17.ps1`；registry `REGISTRY_XIAN_DAILY_2026_09_17` + dt188 + CHANGELOG + `_INDEX-LEDGER-ISSUE-EXPORTS.md`。

7、#79 回执：全部为新建正本/卷宗路径；未覆盖 `docs/issue-exports/*/body.md` 历史主日报正本。

8、分支：归档提交仅 `dev-v2.2`；合流 main 见 `DEV-V2.2-MERGE-CHECKLIST.md` 执行记录。

---

第二段：内部问题状态更新

1. 抖音 100 质询池 — ✅ 已完成（`a8b4bd6`）

2. 官方定义 v1 + 官宣释疑 — ✅ 已完成（`9599652` / `87fb238`）

3. 新华网 xinhuanet 卷宗 — ✅ 已完成（`929b452`）

4. 2026-09-17 主日报 Issue — ✅ 本包补档（#130 · 本 Issue）

5. media-external / v9.2-calibrated / eval_guard — ⏳ 顺延 2026-09-18 主日报 #129 叙述（本日未重复改正本）

6. dev-v2.2 → main 合流 — ⏳ 与 P0 合流清单同步执行
