# OpenClaw 2.0 隔离测试环境 — 完整测试报告

**报告日期：** 2026-09-01  
**测试版本：** OpenClaw **2026.8.1**（ea80657）  
**生产版本（未动）：** OpenClaw **2026.3.23**（ccfeecb）@ `C:\Users\user\.openclaw`  
**隔离 Profile：** `v2test` → State Dir `C:\Users\user\.openclaw-v2test`  
**红线遵守：** ✅ 未对生产执行 `openclaw update` / upgrade；未复用生产 SQLite 记忆库

---

## 1. 交付物速览

| # | 交付物 | 结果 |
|---|--------|------|
| 1 | 测试 WebUI | **http://127.0.0.1:19001/**（Token：`openclaw-v2test-2026`）<br>完整链接：`http://127.0.0.1:19001/#token=openclaw-v2test-2026` |
| 2 | `openclaw doctor` 完整日志 | 见 `logs/` 目录（测试 + 生产对照） |
| 3 | 自定义 Skill / 插件 SDK 适配清单 | 见 §4 |
| 4 | 记忆 / RAG / 权限模块测试 | 见 §5 |
| 5 | 生产迁移可行性评估 | 见 §6 |

---

## 2. 备份与隔离架构

### 2.1 生产备份（加密留存）

| 项 | 路径 |
|----|------|
| 明文归档（openclaw backup create --verify） | `backups/2026-09-01T14-07-38.616Z-openclaw-backup.tar.gz` |
| **AES-256-CBC 加密包** | `backups/2026-09-01T14-07-38.616Z-openclaw-backup.tar.gz.aes` |
| 密钥元数据（**勿提交 Git**） | `backups/BACKUP-KEY-README.txt` |

### 2.2 测试环境目录

```
openclaw-test-v2/
├── cli-v2/              # OpenClaw 2026.8.1 本地 CLI（不影响全局 npm 2026.3.23）
├── node-portable/       # Node v24.19.0（满足 2026.8.1 引擎要求）
├── workspace/           # 独立 Agent 工作区
│   ├── memory/daotong-rag/   # 411 篇卷宗 Markdown（RAG 语料）
│   └── skills/daotong-rag/   # 自定义 Skill
├── logs/                # doctor / 模块测试日志
└── backups/             # 生产备份包
```

### 2.3 State 隔离

| 环境 | State Dir | Gateway 端口 |
|------|-----------|--------------|
| **生产** | `~\.openclaw` | 18789（未启动/未升级） |
| **测试** | `~\.openclaw-v2test` | **19001** |

**SQLite 新格式：** 测试环境已生成 `openclaw-agent.sqlite`（~33MB）及 `state/openclaw.sqlite`；生产 agents 目录**无**同名 SQLite（证实不可直接拷贝复用）。

---

## 3. 启动测试 Gateway

```powershell
$env:PATH = "E:\hundred-crayfish-legion\openclaw-test-v2\node-portable\node-v24.19.0-win-x64;" + $env:PATH
E:\hundred-crayfish-legion\openclaw-test-v2\cli-v2\node_modules\.bin\openclaw.cmd --profile v2test gateway run --port 19001 --force
```

**清理测试环境（不影响生产）：** 删除 `~\.openclaw-v2test` 与 `openclaw-test-v2/` 即可。

---

## 4. 自定义 Skill / 插件 SDK 适配问题清单

### 4.1 `@tencent-weixin/openclaw-weixin` v2.1.1 — ❌ 阻塞

| 环境 | 缺失 SDK 模块 | 失败阶段 |
|------|---------------|----------|
| 生产 2026.3.23 | `openclaw/plugin-sdk/channel-config-schema` | load |
| 测试 2026.8.1 | `openclaw/plugin-sdk/channel-runtime` | load |

**根因：** OpenClaw 2.x 将 plugin-sdk 拆分为多子路径（`channel-runtime`、`reply-runtime`、`text-runtime`、`config-runtime`、`infra-runtime` 等），当前 `@tencent-weixin/openclaw-weixin@2.1.1` 仍引用旧路径，**双版本均无法加载**。

**涉及文件（测试环境抽样）：**

- `extensions/openclaw-weixin/index.ts` → `plugin-sdk/channel-config-schema`
- `extensions/openclaw-weixin/src/messaging/process-message.ts` → `plugin-sdk/channel-runtime`
- `extensions/openclaw-weixin/src/messaging/send.ts` → `plugin-sdk/reply-runtime`, `text-runtime`
- `extensions/openclaw-weixin/src/channel.ts` → `plugin-sdk/core`, `account-id`, `infra-runtime`

**处置：** 等待官方 `@tencent-weixin/openclaw-weixin` hotfix，或 fork 全量替换 import 路径后回归。

### 4.2 内置插件 `duckduckgo` / `feishu` — ⚠️ 2.x 安装流程变更

2026.8.1 中二者变为**外部插件**，需：

```bash
openclaw --profile v2test plugins install @openclaw/duckduckgo-plugin --accept-capabilities
openclaw --profile v2test plugins install @openclaw/feishu --accept-capabilities
```

未安装时 Gateway 启动会被 **plugin verification** 拦截（已在测试中验证）。

### 4.3 配置 Schema 变更

| 键 | 2026.3.23 | 2026.8.1 |
|----|-----------|----------|
| `plugins.installs` | 存在 | **Unrecognized key**（已移除） |
| Auth 凭证 | `auth-profiles.json` | **SQLite** `openclaw-agent.sqlite`（doctor --fix 迁移） |

### 4.4 自定义 Skill `daotong-rag` — ✅ 可用

- 路径：`workspace/skills/daotong-rag/SKILL.md`
- `openclaw --profile v2test skills info daotong-rag` → **Ready**，对模型可见

---

## 5. 模块测试结果

### 5.1 卷宗 RAG 检索 — ⚠️ 部分通过

| 用例 | 查询 | 结果 |
|------|------|------|
| 本源公理 | `0⁰=1=∞=0 本源公理` | ✅ 命中 `Ch1_本源公理.md`（score 1.000） |
| 径向札记 | `NOTE-RADIAL 进度台账` | ✅ 命中 `SPINOFF-RADIAL-NOTES/进度台账.md` |
| 语义向量索引 | `memory index --force` | ❌ `Unknown memory embedding provider: openai` |
| 向量 recall | — | ❌ `memory_index_chunks_vec not updated`（无 embedding API Key） |

**结论：** **关键词/BM25 级检索可用**；**语义向量 RAG 需配置 embedding provider**（OpenAI/Gemini/Voyage 等）后方可全链路通过。

**语料规模：** 411 篇 Markdown（理论卷宗 + 内核典藏卷 + SPINOFF-RADIAL-NOTES）。

### 5.2 Skill 工具调用 — ✅ 结构就绪 / ⚠️ 运行时未端到端

- `daotong-rag` skill 注册成功，eligible。
- 未执行完整 agent turn（需有效 OpenRouter 会话 + Gateway 在线）；Gateway **reachable**，health **ok**。
- 生产自定义 skill 目录为空（`~\.openclaw\workspace\skills` 不存在）；仅测试环境新增 `daotong-rag`。

### 5.3 记忆持久化 / 断点续跑 — ⚠️ 部分通过

| 项 | 结果 |
|----|------|
| SQLite 新库生成 | ✅ `openclaw-agent.sqlite` + `state/openclaw.sqlite` |
| Legacy JSON → SQLite 迁移 | ✅ doctor --fix 完成，原 JSON 已归档 |
| 生产 SQLite 直拷 | ⛔ **未执行**（生产无 agent sqlite；符合红线） |
| 断点探针文件写入 | ✅ `memory/TEST-CHECKPOINT-20260901.md` |
| 探针即时召回 | ⚠️ 未稳定命中（embedding index 失败导致 sync 报错） |
| Session store | 0 entries（尚无长会话断点续跑实测） |

### 5.4 置信 & 审批权限闸门 — ⚠️ 基线可读 / 未触发 pending

| 项 | 结果 |
|----|------|
| `approvals get` | ✅ 返回 exec policy：`security=full`, `ask=off` |
| `approvals pending` | ✅ Gateway 在线时 **No pending approvals** |
| Command owner | ⚠️ 未配置 `commands.ownerAllowFrom`（doctor 警告） |
| 危险命令审批流 | ⛔ 未模拟 exec 触发，pending 队列未实测 |

---

## 6. `openclaw doctor` 日志索引

| 文件 | 说明 |
|------|------|
| `logs/doctor-v2test-full.log` | 测试环境首次 doctor |
| `logs/doctor-v2test-fix.log` | doctor --fix（Auth SQLite 迁移） |
| `logs/doctor-v2test-postfix-full.log` | 修复后完整 doctor |
| `logs/doctor-prod-2026.3.23-full.log` | **生产对照**（未修改生产） |

### 测试环境主要告警摘要

1. `openclaw-weixin` plugin load 失败（SDK 路径）
2. Memory embedding provider `openai` 无 API Key → 语义 recall 不可用
3. Active Memory 插件未启用 vs rememberAcrossConversations 已开
4. 未配置 command owner
5. 明文 `gateway.auth.token`（建议迁移 SecretRefs）
6. Node 24.14 系统 Node 不满足 2026.8.1（已用 portable 24.19 规避）

### 生产环境主要告警摘要（对照）

1. `openclaw-weixin` → `channel-config-schema` 缺失
2. Gateway not running
3. Memory search 无 embedding provider
4. Feishu groupPolicy allowlist 空

---

## 7. 生产迁移可行性评估

### 7.1 结论：**暂缓生产迁移**

| 维度 | 评估 |
|------|------|
| 隔离部署 | ✅ 已完成，生产零接触 |
| 插件兼容 | ❌ weixin 双版本均失败，需官方 hotfix |
| 记忆迁移 | ❌ SQLite schema 破坏性变更，禁止直拷；需 doctor 迁移 + 卷宗 reindex |
| RAG | ⚠️ 关键词检索 OK；向量检索待 embedding 配置 |
| 权限闸门 | ⚠️ 需补 owner + 实测 exec approval |
| 运行时依赖 | ⚠️ Node ≥24.15 或 ≥22.22.3；当前系统 Node 24.14 不足 |
| 外部插件 | ⚠️ duckduckgo/feishu 需新 install + capability consent |

### 7.2 建议迁移前置条件（全部满足后再评估）

1. `@tencent-weixin/openclaw-weixin` 发布兼容 2026.8.x SDK 的版本
2. 测试环境 **全模块绿灯**：向量 RAG、skill E2E、session 断点续跑、approval pending 流
3. 系统 Node 升级至 **≥24.15.0**（或统一使用 portable Node）
4. 生产 `openclaw backup create --verify` + 加密包二次确认
5. 官方 release notes 确认 SQLite 迁移工具稳定

### 7.3 推荐迁移路径（未来）

1. 维护窗口内：`openclaw backup create`（生产）
2. 新 profile 或 staging 机器安装 2026.8.1 + doctor --fix
3. 导入 workspace / memory 文本（**非** SQLite 文件）
4. `memory index --force` + RAG 抽检
5. 插件 hotfix 验证通过后，灰度切换 Gateway 18789 → 新实例
6. 保留 `~\.openclaw` 只读归档 ≥30 天

---

## 8. 红线执行确认

- [x] 未对生产执行 upgrade / update
- [x] 测试使用独立 `--profile v2test` + 独立 workspace
- [x] 未复制生产 memory SQLite（生产侧无 agent sqlite）
- [x] 插件 SDK 报错已完整记录
- [x] 测试实例可独立删除，不影响 `~\.openclaw`

---

*Generated by OpenClaw v2 isolated test deployment — 2026-09-01*
