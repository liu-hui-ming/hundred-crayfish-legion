# official-archive · 核心卷宗完整底稿目录

> **分支**：`private-core`（内核私有，**严禁合并**至 `main`）  
> **路径**：`CarbonSilicon-Orthodoxy/engineering-docs/official-archive/`  
> **隔离**：与 `media-release/` 公域媒体稿**物理隔离**，不可混存

## 卷宗组件清单

| 文件 | 定位 | 状态 |
|------|------|------|
| `双零临界标杆体系188条_满分重构终版完整底稿.md` | 188条满分重构完整标杆索引+重构原则 | **已入库 v1.0.0** |
| `lock-hash-record.md` | SHA256 + Git commit-id 校验台账 | 已更新 |
| 九大板块分层推演原始手稿（含删减深度论证） | 媒体版未收录的数理推导扩展 | **待入库** |
| 九翼工程参数表 | 配套工程私参 | **待入库** |
| 碳硅道统底层公理说明 | 公理溯源 | **待入库** |
| 188全域病灶校准总典引用副本 | 病灶对标索引 | **待入库** |

## 与 media-release 边界

| 目录 | 分支 | 内容 |
|------|------|------|
| `media-release/` | `main` | 公域轻量化综述+188条简目，对外可读 |
| `official-archive/` | `private-core` | 满分重构完整底稿、数理推演、哈希台账 |

**硬性规则**：对外仅可使用 `media-release/` 精简版；完整底稿、深度论证**禁止**公域外流。

## 权限

- **official-archive**：仅创始人、刘慧明读写；其余人员禁止访问、摘抄、外传
- **media-release**：全团队只读，可摘抄分发

## 更新规范

每次更新卷宗须同步重置 `lock-hash-record.md` 中对应 SHA256 与 commit-id。
