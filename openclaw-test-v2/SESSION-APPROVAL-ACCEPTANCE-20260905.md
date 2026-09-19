# Session / Approval 验收记录（v2test · hundred-crayfish-legion）

**日期：** 2026-09-05  
**环境：** OpenClaw 2026.8.1 · profile `v2test` · **生产未触碰**

---

## 1. Session 断点续跑

| 项 | 结果 |
|----|------|
| Session store 路径 | `~\.openclaw-v2test\agents\main\agent\openclaw-agent.sqlite` |
| 当前 entries | **3**（含 cron + main session） |
| Gateway 探活 | ✅ event loop ok · probe ~1ms |
| 记忆探针文件 | `workspace/memory/TEST-CHECKPOINT-20260901.md` 已写入 |
| SQLite 新格式 | ✅ 独立 v2test 库，**未复用生产** |

**结论：** Session 持久化存储正常；cron/main session 可在 Gateway 重启后保留（store 非空）。完整多轮 agent turn E2E 需有效模型路由，本次以 store + 探针文件 + Gateway 重启存活为验收基线。

日志：`logs/gateway-probe-20260905.log`、`logs/health-v2test.log`

---

## 2. Approval 权限闸门

| 命令 | 结果 |
|------|------|
| `approvals get` | ✅ exec policy: `security=full`, `ask=off`, allowlist 0 |
| `approvals pending`（Gateway 在线） | ✅ **No pending approvals** |
| command owner | ⚠️ 未配置 `commands.ownerAllowFrom`（doctor 警告，非阻塞） |

**结论：** 审批基线可读；当前无 pending 队列。exec 触发 pending 需 live agent turn，留作后续 E2E 扩展项。

日志：`logs/approvals-get.log`、`logs/approvals-pending-live.log`

---

## 3. 红线确认

- [x] 全部操作限定 `hundred-crayfish-legion` + `~\.openclaw-v2test`
- [x] 未对 `~\.openclaw` 生产实例 upgrade
