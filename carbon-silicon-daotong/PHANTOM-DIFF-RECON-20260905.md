# carbon-silicon-daotong · phantom diff 对账（2026-09-05）

**目的：** 本地工作区 Ch0–Ch5 与 README.md SSOT MD5 指纹双向对账，识别 phantom diff（台账/指纹与磁盘不一致）。

**SSOT 来源：** `carbon-silicon-daotong/README.md` §定稿全局MD5指纹

---

## 对账结果

| 文件 | README MD5 (SSOT) | 本地 MD5 (2026-09-05) | 状态 | 说明 |
|------|-------------------|----------------------|------|------|
| `理论卷宗/Ch0_方法论自白.md` | `717e39f…14d1c` | `4f730b2f…8a40` | ❌ MISMATCH | 正文相对 SSOT 指纹已漂移 |
| `理论卷宗/Ch1_本源公理.md` | `41d14856…6cd3` | `dd4f6a2c…d649` | ❌ MISMATCH | 同上 |
| `理论卷宗/Ch2_理论论战.md` | `656bdea1…c612` | — | ❌ PHANTOM | **磁盘为 `Ch2_演化之战.md`**，SSOT 文件名不一致 |
| `理论卷宗/Ch3_硬件架构.md` | `5ba95fc1…c41e` | `fe88bc40…4d50` | ❌ MISMATCH | |
| `理论卷宗/Ch4_实验设计_终稿.md` | `2b82ddb1…5fcb` | `bc42f7e5…ecbd` | ❌ MISMATCH | |
| `理论卷宗/Ch5_伦理契约.md` | `a92ad7bc…f5e4` | `7ce55e83…a984` | ❌ MISMATCH | |
| `CH0-CH5进度台账.md` | `804907ea…dcaa` | `07f90435…ee18` | ❌ MISMATCH | 台账内容已更新，指纹未同步 |

---

## 结论

1. **7/7 项与 README SSOT 指纹不一致** — 不得标记「远程 SSOT 已对齐」。
2. **Ch2 文件名 phantom：** SSOT 登记 `Ch2_理论论战.md`，工作区存在 `Ch2_演化之战.md`（及/或 `Ch2_理论论战.md` 需人工确认 canonical 名）。
3. **处置建议（禁止覆盖 V1.0 初稿）：** 若当前磁盘为迭代版本，应新建独立版本文件并更新 SSOT 指纹块；合流前禁止 silent overwrite。

**执行环境：** 本地对账 only · 生产 OpenClaw 未写入
