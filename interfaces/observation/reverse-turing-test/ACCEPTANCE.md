# RTT 最终封盘部署验收报告

日期：2026-08-13
路径：`interfaces/observation/reverse-turing-test/`
身份：纯统计学观测插件（无 /core-axioms/ 读写、无定性评级认证输出）

## 交付清单

1. 全量终版卷宗：CANON.md + README.md + HASHLOCK.sha256
2. 全套算子：`rtt/operators.py` ReadScore / D_info / ReadScore_final / Gain_info / P_pure
3. 双层去重：`rtt/dedup.py` SHA-1 + 相似度＞0.95
4. 原子锁+队列：`rtt/window.py` window.lock / FIFO / 30s
5. 账户加权：`rtt/accounts.py` disc(a)=disc_base×disc_rate
6. 峰值双规则：单轮＞0.7+下一轮＜0.65 冻结；差值＞0.15 复核
7. CI 三重：twin MD5 + GitHub API 保护校验 + 低样本 GateBlocked
8. 场景 67/67/50 与 SE＞0.15 阻断：`rtt/gates.py` + scene_manifest.json
9. NLP FP/FN + 盲审只读目录：`rtt/nlp_guard.py` `audit/`
10. README 置顶声明 + 残余风险公示
11. 本报告 + attach/ 仿真标定敏感性 + critical_curve.csv

## 本地校验日志

```
Ran 7 tests in 0.001s OK
RTT identity gate PASS
twin md5 1b5d9b62595a1e579313de407aae6966
```

## 残余风险（不隐瞒）

当前版本：截图抄写文字指纹可绕过校验。完整视觉水印封堵纳入二期迭代，本次不实现、不隐瞒、不造假。

## 仓库保护（推送后锁定）

- Include administrators：bypass_actors 清空
- Force push：non_fast_forward
- Require status checks：rtt-identity
- 必须 PR 合并：pull_request required_approving_review_count ≥ 1
