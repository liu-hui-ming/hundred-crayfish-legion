# spinoff / inquiry 合流前 · PDF 抽取缓存清理清单（2026-09-05）

**原则：** 合流入库前清除 PDF 抽取缓存，避免 phantom 文件进入 git 索引。

---

## 待清理目录（仓库根 · 未跟踪）

| 路径 | 类型 | 动作 |
|------|------|------|
| `_extract_13/` | PDF 抽取缓存 | ⏳ 合流前删除或 `.gitignore` 排除 |
| `_extract_188/` | PDF 抽取缓存 | ⏳ 同上 |
| `_extract_5/` | PDF 抽取缓存 | ⏳ 同上 |
| `_extract_54/` | PDF 抽取缓存 | ⏳ 同上 |
| `_extract_debate/` | PDF 抽取缓存 | ⏳ 同上 |
| `_extract_ninewing/` | PDF 抽取缓存 | ⏳ 同上 |
| `_extract_sic6/` | PDF 抽取缓存 | ⏳ 同上 |

## 待排除 PDF 原稿（根目录 untracked · 不入库）

`1-120.pdf`, `1-99.pdf`, `10大独立典籍.pdf`, `10篇.pdf`, `10问答.pdf`, 等 — 保留本地，**禁止**与 spinoff/inquiry md 合流提交。

---

**状态：** 清单已登记；物理删除留待合流窗口执行（避免误删未备份原稿）。
