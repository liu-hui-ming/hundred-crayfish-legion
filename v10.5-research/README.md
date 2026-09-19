# v10.5-research · CANONICAL-v3.1（内部研究基线）

**System_Tag:** `CANONICAL-v3.1`  
**性质:** 私有仓内部封存基线 · **不对外 GitHub Release · 不公开宣传**  
**用途:** 01 推演 / 红蓝反向校准前置归档；基线冻结后修改须新建版本，禁止原地篡改已打 tag 内容。

## 目录清单（9 文件）

| # | 文件 | 状态 |
| --- | --- | --- |
| 1 | `README.md` | 本说明 |
| 2 | `check_isolation.sh` | 占位 · 待替换正本 |
| 3 | `full_bootstrap.sh` | 占位 · 待替换正本 |
| 4 | `veto_tee_stub.py` | 占位 · 待替换正本 |
| 5 | `enclave_entry.py` | 占位 · 待替换正本 |
| 6 | `test_iron_laws.py` | 占位 · 待替换正本 |
| 7 | `v105-enclave.manifest.template` | 占位 · 待替换正本 |
| 8 | `manifest.json` | 基线元数据 · 哈希待 `full_bootstrap.sh` 回填 |
| 9 | `yc1_statistics.json` | 试点数据 · 待替换正本 |

## 后续步骤（源码到位后）

1. 用正本 **覆盖** 上表 2–9（保持 UTF-8 无 BOM）。
2. `chmod +x *.sh`（Git Bash / Linux）→ `./full_bootstrap.sh`。
3. 确认 stub 全 PASS；hardware 仅 quote 层 `NotImplementedError` 为预期。
4. `git commit` + `git tag v10.5-research-CANONICAL-v3.1` + `git push origin main` + push tag。

## 仓库

`https://github.com/liu-hui-ming/hundred-crayfish-legion` · 路径 `v10.5-research/`
