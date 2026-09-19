# carbon-silicon-daotong · phantom diff 对账（2026-09-07 更新）

**目的：** 本地 Ch0–Ch5 与 README.md SSOT MD5 指纹对账；裁定 canonical 文件名与指纹同步策略。

**SSOT 来源：** `carbon-silicon-daotong/README.md` §定稿全局MD5指纹

---

## 1. Ch2 canonical 裁定（2026-09-07）

| 项 | 裁定 |
|----|------|
| **canonical 文件名** | `理论卷宗/Ch2_理论论战.md` |
| 依据 | 磁盘唯一正本；内容与 SSOT 登记标题一致；`Ch2_演化之战.md` 为历史 phantom 别名，**不采用** |
| 处置 | 若存在 `Ch2_演化之战.md` 副本，保留为只读别名或移入归档说明，**禁止覆盖** `Ch2_理论论战.md` |

---

## 2. 对账结果（2026-09-05 基线 · 2026-09-08 复核）

| 文件 | README MD5 (SSOT) | 本地状态 | 说明 |
|------|-------------------|----------|------|
| Ch0–Ch5 正文 | 见 README 块 | ✅ **MATCH** | 2026-09-08 SSOT 指纹同步 commit |
| CH0-CH5进度台账 | `07f90435…ee18` | ✅ **MATCH** | 台账指纹已同步 |
| Ch2 文件名 | `Ch2_理论论战.md` | ✅ **已对齐** | phantom 别名问题已裁定 |

---

## 3. SSOT 指纹同步策略（禁止覆盖 V1.0 初稿）

1. **V1.0 初稿永久封存** — `Ch*_*.md` 定稿正文禁止直接 overwrite；迭代须新建 `*-V1.1.md` / 独立版本文件。
2. **指纹更新路径** — 仅当 canonical 文件经人工确认定稿后，在 **独立 commit** 中更新 `README.md` §定稿全局MD5指纹 对应行（或新建 `测试规范/full_archive_md5_fingerprint.txt` 增补块），commit message 须注明「SSOT 指纹同步 · 非正文改写」。
3. **phantom diff 闭环** — 每次指纹同步后复跑 `certutil -hashfile … MD5`，更新本文件 §2 表格为 MATCH。
4. **合流门禁** — spinoff/inquiry 合流前，Ch0–Ch5 phantom diff 未 CLOSED 则不得标记 SSOT 已对齐。

---

## 4. 结论

- Ch2 canonical：**`Ch2_理论论战.md`**
- 全文指纹块：**2026-09-08 SSOT 指纹同步 commit 已 MATCH**
- 生产 OpenClaw：**未写入**

**前版：** 2026-09-05 初稿 · Ch2 曾报 `Ch2_演化之战.md` phantom → 本版已裁定修正
