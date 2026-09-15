# 百剑刺针 · 待发布链回填结项（2026-09-05）

**范围：** 创业邦 843850、36kr v2（3957153109622150）黄金 24h 同步链  
**原则：** 首发链已上线仅回填真实 URL；公众号/知乎未发布禁止虚构链接

---

## 1. 首发链复核

| 首发媒体 | 原文链接 | 复核结果 | 本地快照 |
| -------- | -------- | -------- | -------- |
| 创业邦 843850 | https://www.cyzone.cn/article/843850.html | ✅ 可访问，标题与台账一致 | `snapshot/snapshot-cyzone-v1.html` |
| 36kr v2 | https://36kr.com/p/3957153109622150 | ✅ 台账已登记；抓取遇 WAF，以本地快照为准 | `snapshot/snapshot-36kr-v2.html` |
| Wayback（创业邦） | https://web.archive.org/web/20260821125432/https://www.cyzone.cn/article/843850.html | ✅ 已完成 | 见 `golden-24h-checklist.md` |

**结论：** 两条首发链均已上线并完成台账登记，无需补链。

---

## 2. 同步链（公众号 / 知乎）— 阻塞于人工发布

| 稿件 | 平台 | 台账状态 | 同步稿 | 阻塞原因 |
| ---- | ---- | -------- | ------ | -------- |
| 算力堆不出"灵魂"…（创业邦版） | 碳硅道统公众号 | 【待发布后补链】 | `golden-24h-cyzone843850-wechat-zhihu.md` | 待人工粘贴发布 |
| 同上 | 知乎 | 【待发布后补链】 | 同上 | 待人工粘贴发布 |
| 算力堆不出"灵魂"…（36kr v2 版） | 碳硅道统公众号 | 【待发布后补链】 | `golden-24h-36kr-v2-wechat-zhihu.md` | 待人工粘贴发布 |
| 同上 | 知乎 | 【待发布后补链】 | 同上 | 待人工粘贴发布 |

**结项说明：** 同步链 4 行台账保持「待发布」占位，不写入虚构 URL。发布完成后：

1. 将四条真实 URL 写入 `sync/golden-24h-published-urls.json`
2. 执行 `python scripts/backfill_golden24h_ledger_snapshots.py --commit`（校验正文含「算力堆不出」或「碳硅道统」并生成快照）
3. push `dev-v2.2`

**2026-09-15 状态：** 公开检索 / Sogou 微信 / Bing 仍未命中可核验链接；阻塞于人工提供 URL。

---

## 3. 关联台账

- 媒体信源：`dossier/broadsword-100/broadsword-media-ledger.md` §待发布链回填进度
- 执行清单：`sync/golden-24h-checklist.md`、`sync/golden-24h-checklist-36kr-v2.md`
