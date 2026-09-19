# archive/media-external · 对外媒体卷宗（工程层）

叙事层正文正本见 `dola-carbon-silicon-framework/docs/`；本目录仅存 **快照、回链元数据、双轨镜像** 与 **全局 manifest**。

## 全局清单

| 文件 | 说明 |
| --- | --- |
| [`manifest.json`](./manifest.json) | 卷宗级 SHA256 汇总（rmzxw + 白皮书双轨） |

## 命名模板（P2 统一）

| 类型 | 模板 |
| --- | --- |
| 正文镜像 | `{YYYYMMDD}-{source}-{slug}.md` |
| 回链元数据 | `{YYYYMMDD}-{source}-{slug}-source-metadata.json` |
| 全页快照 | `{YYYYMMDD}-{source}-{slug}-snapshot.png` |
| 完整网页包 | `{YYYYMMDD}-{source}-{slug}.mhtml` |
| 历史/附件 | `attachments/{legacy-filename}` |

## 子卷宗

| 路径 | 说明 |
| --- | --- |
| [`rmzxw/`](./rmzxw/) | 人民政协网 2026-09-16 稿件 |
| [`whitepaper/`](./whitepaper/) | 白皮书 T-02/Y-04 双轨镜像 |

## 校验

```bash
python scripts/hash_integrity_checker.py
python scripts/_build_media_external_manifest.py
```

编码：UTF-8 无 BOM。分支：仅 `dev-v2.2`；**禁止**未经指令 push `main`。
