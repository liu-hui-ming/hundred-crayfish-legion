复核类型：仓库内镜像 vs 新福建网同源稿（非站点直抓替代）

采样标识（归档正本，未修改）：

12	安徽日报客户端首发	https://web.ahnews.com.cn/news?id=537412

12	安徽日报客户端首发	https://web.ahnews.com.cn/news?id=537430

对照正本：

- docs/issue-exports/xian-daily-2026-09-10-ahnews-537412/body.md
- docs/issue-exports/xian-daily-2026-09-10-ahnews-537430/body.md
- docs/issue-exports/xian-daily-2026-09-10-newfj-115754/body.md
- docs/issue-exports/xian-daily-2026-09-10-newfj-115755/body.md

---

## 结论（2026-09-15）

1. Playwright 访问 `web.ahnews.com.cn/news?id=537412` 与 `537430`：**ERR_CONNECTION_CLOSED**（与 Batch #123 归档时一致）。
2. 去掉各 `body.md` 头部采样标识行后，安徽 archived 正文与同期新福建网正文 **逐字一致**（diff ratio 1.0）。
3. **未发现内容差异** → 按 XIAN-ARCHIVE-HARD-RULES **未**新建 `ahnews-*` 迭代文件夹，**未覆盖**原归档正本。
4. **待办（需本地浏览器）**：若安徽日报客户端页面正文与上述镜像不一致，请提供差异片段，再新建独立 slug 文件夹留存迭代版本。

Issue 日报锚点：https://github.com/liu-hui-ming/hundred-crayfish-legion/issues/123
