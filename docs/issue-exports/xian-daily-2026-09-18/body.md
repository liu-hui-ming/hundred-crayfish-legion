采样标识（verbatim）：

```
标题：[P1-Roadmap] 2026-09-18 XIAN项目日报 | media-external政协网全页快照 + 白皮书96/100双轨 + 2026-09-17 doctrine闭环补记
资源：XIAN项目日报 · hundred-crayfish-legion
回链：（Issue 发布后回填）
归档路径：docs/issue-exports/xian-daily-2026-09-18/
```

---

1、P0 · **media-external · 人民政协网全页快照卷宗**：新建 `archive/media-external/rmzxw/`；对 https://www.rmzxw.com.cn/c/2026-09-16/3976199.shtml 抓取 **full-page PNG + MHTML**（Playwright CDP `Page.captureSnapshot`）；`20260916-rmzxw-ai-simulate-awareness-boundary-source-metadata.json` 写入 canonical URL、HTTP 状态、page_title、叙事层正文路径；历史 HTML 快照迁入 `attachments/`（正文与附件路径分离）；采样 `20260916-rmzxw-ai-simulate-awareness-boundary`；PNG SHA256 `11df06c806a02c6f1875544348dd1cacd5ae0e15c85bc291515ab4b3f9cdd4b5`、MHTML `182c8f23209ae3ee9412e208e4d213ca04515e4ea63a2cf7d120a50f91a73993`；叙事正本仍在 `dola-carbon-silicon-framework/docs/media-clipping/rmzxw/`（未覆盖改正文）。

2、P0 · **白皮书 T‑02/Y‑04 双轨入库**：公域 **96 分纯白版** `…-T02Y04-public-domain-96.md`（剔除 Git/SHA 内核台账行，SHA256 `28f5b9e39ea71e97102a9e71b5aff56d66d9ee6e8748a54ef911541b26b5234b`）；GitHub **100 分完整版** `…-T02Y04-github-archive-100-full.md`（保留台账字段 + 归档说明尾注，SHA256 `90d1b9e2f2c2ee6e5a3f5d59e669bffd93770d3cb089a4164c50e01dc774b15`）；双轨同步镜像 `archive/media-external/whitepaper/`；历史单文件正本 `carbon-silicon-daotong-silicon-civilization-axiom-whitepaper-public-media.md` 仍只读（SHA256 `92a8b82d…` · commit afb429f）。

3、P0 · **media-external 全局 manifest**：`archive/media-external/manifest.json`（schema `manifest.global.v1`）汇总 rmzxw 卷宗 + 白皮书双轨条目、各文件 SHA256、`ch_series_ref`（CH-MEDIA-EXTERNAL-*）；manifest 自身 SHA256 归档后写入台账；脚本 `scripts/_build_media_external_manifest.py` · `scripts/hash_integrity_checker.py` 本地预跑 **PASS**。

4、P0 · **XIAN 一日一发（本日）**：本稿件 `docs/issue-exports/xian-daily-2026-09-18/`；脚本 `scripts/publish_xian_daily_issue_2026_09_18.ps1`；registry `REGISTRY_XIAN_DAILY_2026_09_18` + `CHANGELOG.md` + `_INDEX-LEDGER-ISSUE-EXPORTS.md`；与 media-external 归档 **同日 commit 链闭合**（不延后积压）。

5、P1 · **2026-09-17 doctrine / 质询补记（前日已 push dev-v2.2）**：100 质询抖音池 `content/comment-pool/douyin-100-question-series/`（c64c56f→a8b4bd6）；官方定义 v1（9599652）；官宣释疑 `canonical/charters/`（87fb238）；新华网 `archive/media/xinhuanet/`（929b452）；**本日未改正本**，仅纳入日报状态闭环。

6、P1 · **CH 系列卷宗归属**：`carbon-silicon-daotong/CH0-CH5进度台账.md` 增补 **CH-MEDIA-EXTERNAL-RMZXW-T02Y04**、**CH-MEDIA-EXTERNAL-WHITEPAPER-T02Y04**；附件（PNG/MHTML/HTML）仅驻留 `archive/media-external/**/attachments/`，正文 md 与 narrative 层路径分离。

7、P2 · **命名规范模板**：`archive/media-external/README.md` 统一 `{YYYYMMDD}-{source}-{slug}-snapshot.png|.mhtml|source-metadata.json`；P2 完整性脚本 `hash_integrity_checker.py` 已可一键校验 manifest 条目。

8、**#79 回执**：media-external 为增量卷宗；未覆盖 `docs/issue-exports/*/body.md` 正本；未虚构 rmzxw URL；**未 push origin/main**（仅 dev-v2.2 工作分支提交）。

---

第二段：内部问题状态更新

1. 政协网 HTML 快照（09-16 初版） — ✅ 已完成（7a665e2 · Issue #127）

2. 政协网 **全页 PNG+MHTML + source-metadata + 全局 manifest** — ✅ 本日闭合（media-external/rmzxw）

问题简述：初版仅单文件 HTML，未满足「完整网页快照 + 回链元数据 + 全局清单」P0 要求。  
状态：已闭合。  
处理方案：`archive/media-external/rmzxw/` 双快照 + metadata；legacy HTML 降格为 attachments 引用。

3. 白皮书单轨正本（止于 4.10） — ✅ 前序已完成（afb429f · #126）

4. 白皮书 **96/100 双轨 + media-external 镜像** — ✅ 本日闭合

备注：96 轨供公域传播；100 轨供 GitHub 可验证归档；后续章节仍须 **新文件名** 迭代，禁止改正本。

5. 2026-09-17 主日报 Issue — ⏳ 待补发（可选合并 #129 叙述）

6. 2026-09-08～09-14 主日报 backlog — ⏳ 待批量指令

7. dev-v2.2 → main 合流 — ⏳ 待「执行合流」（`DEV-V2.2-MERGE-CHECKLIST.md`）

8. UTF-8 / 双基线哈希历史卷宗抽检 — 🔄 本日补全 media-external；其余卷宗按 P1.2 滚动补 manifest 字段
