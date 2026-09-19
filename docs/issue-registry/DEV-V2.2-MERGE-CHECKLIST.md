# dev-v2.2 → main 合流前闭环清单

**更新：** 2026-09-19 · 合流执行前核对 `origin/dev-v2.2` @ `6612fd9` 及后续 P0 提交

## XIAN 媒体批次

- [x] Batch #123 · Issue #121 · 7/7 · `xian-daily-2026-09-10-*`
- [x] Batch #124 · Issue #122 · 9/9 · `xian-daily-2026-09-11-*`
- [x] Batch #125 · Issue #124 · 3/3 · `xian-daily-2026-09-14-chinacom-*`（#125 已关闭为重复）

## dt188 台账

- [x] #121 Batch #123
- [x] #122 Batch #124
- [x] #123 日报 2026-09-15
- [x] #124 Batch #125

## axium REGISTRY

- [x] `REGISTRY_XIAN_DAILY_2026_09_10_MEDIA_*` ×7
- [x] `REGISTRY_XIAN_DAILY_2026_09_11_MEDIA_*` ×9
- [x] `REGISTRY_XIAN_DAILY_2026_09_14_MEDIA_CHINACOM_*` ×3
- [x] 日报 `REGISTRY_XIAN_DAILY_2026_09_15` · #123
- [x] 日报 `REGISTRY_XIAN_DAILY_2026_09_16` · #128
- [x] 日报 `REGISTRY_XIAN_DAILY_2026_09_17` · #130（补档）
- [x] 日报 `REGISTRY_XIAN_DAILY_2026_09_18` · #129
- [x] engineering-layer · `eval_baseline_batches` · eval_guard（20260918 采样）

## 已知占位（不阻塞合流决策）

- golden-24h 四条公众号/知乎：`broadsword-media-ledger.md` 待补链（`golden-24h-published-urls.json` 空）
- 主日报 backlog 2026-09-08～09-14：待下发指令

## 合流动作

- [x] **2026-09-19** PR/merge `dev-v2.2` → `main` · merge commit `82592d2` · 冲突文件以 dev-v2.2 为准消解
- [ ] 合流后逐链 HTTP 复核 Batch 外链（待运维抽测）
