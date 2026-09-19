# v10.5-research：TEE 气闸隔离基线

**System Tag: CANONICAL-v3.1**  
**创立人: 黄清佳（碳硅道统）**  
**基线版本: v10.5-research（MVP 正式冻结版）**

## 法理定位

本文档为 **v10.5-research 工程基线官方归档声明书**。  
对外定义体系边界、固化信任根规则、公示三条隔离铁律、锁定双模式运行契约、明确版本迭代路线、坦诚全部已知局限。

本仓库不是普通实验代码，是**可审计、可复现、可校验、可追溯的碳硅工程实证基线**。

---

## 一、架构总览

v10.5-research 实现 **YC-1研究域 / KP-1生产域** 刚性隔离，构建AI体系「研究-生产解耦」硬件信任基座。

核心目标：依靠**三条代码级铁律**，根除三类风险：

1. 研究域YC-1敏感字段泄露流入KP-1生产链路
2. 假说边界 `G∉RE` 被隐式当成绝对真值直接使用
3. 研究输出缺少「基于测试集/合成样本」免责声明

### 分层安全架构

【非信任主机域 Host】  
数据集生成、采样、统计计算、业务上层逻辑  
yc1_collect、统计模块全部运行于此  

↓ stdin/stdout 纯JSON消息（原始数据集绝不传入Enclave）

【可信执行域 Enclave】  
仅运行三件核心逻辑  

1. 三条隔离铁律校验 verify_isolation_boundary  
2. SHA256哈希摘要计算  
3. TEE-Quote凭证生成调度  

**架构铁则**

- 原始数据集永远不进入Enclave内存，规避内存泄露、侧信道风险  
- 业务校验逻辑代码固化，硬件底层升级，上层契约不变  
- 信任根只升级底座，不修改业务公理契约  

---

## 二、双模式运行契约（体系核心）

整体原则：**业务逻辑100%一致，仅凭证生成层存在差异**

### TEE_MODE=stub（MVP开发模式）

- 业务校验：完整实现三条铁律，与硬件模式代码同源  
- Quote凭证：软件模拟STUB_QUOTE，附带开发警告  
- 信任等级：仅用于本地开发自测，**严禁对外审计使用**  
- manifest标记：`mode:"stub"`，附带风险提示文本  

### TEE_MODE=hardware（Beta硬件模式，待落地）

- 业务校验：复用同一套代码，零修改、零逻辑漂移  
- Quote凭证：对接SGX-DCAP生成硬件可信凭证  
- 信任等级：硬件信任根支撑，支持第三方外部审计  
- manifest标记：`mode:"hardware"`，填入MRENCLAVE指纹  

> 核心契约：两种模式业务输出必须完全一致；硬件模式尚未实现时，仅Quote层抛出NotImplementedError属于预期行为，业务校验一旦失败即为严重bug。

---

## 三、三条工程铁律（代码硬约束）

### 铁律1｜YC-1不入合取

KP-1_MAIN生产上下文**强制拦截**：  
`G_component_true` / `G_observable_combined` / `yc1_appendix` / `structure_tags` / `difficulty_tier`  

> 研究域专属字段禁止直接混入生产链路。

### 铁律2｜G∉RE恒为假说

**任意上下文都拦截绝对真值标签**：  
`G_provable` / `G_is_decidable` / `oracle_final_answer` / `re_complete_groundtruth`  

> 研究假说不能直接当作客观真理。

### 铁律3｜研究输出必须附带限定声明

YC-1_OUTPUT输出必须包含`disclaimer`字符串，且至少包含关键词`relative`或者`synthetic`，否则直接阻断输出。  

> 明确结果适用边界，杜绝结论泛化滥用。

---

## 四、快速启动｜一键全链路闭环

### 环境依赖

- Python3.8+  
- bash  
- pytest（脚本会自动安装）  
- git（可选，用于回填commit基线指纹）  

### 完整一键流水线

```bash
chmod +x check_isolation.sh full_bootstrap.sh
./full_bootstrap.sh

TEE_MODE=stub python3 -m pytest test_iron_laws.py -v
TEE_MODE=hardware python3 -m pytest test_iron_laws.py -v
```

### 基线哈希手动校验

```bash
sha256sum yc1_statistics.json veto_tee_stub.py test_iron_laws.py
```

输出哈希需要和 manifest.json 内 baseline_hashes 一一对应。

---

## 五、版本迭代冻结路线

**MVP｜v10.5-research（当前基线）**

- [x] 三条铁律完整代码实现  
- [x] stub/hardware双模式契约框架  
- [x] 全套正向、反向、边界测试用例  
- [x] SHA256全局哈希锚定  
- [x] CI自动化流水线脚本  
- [x] manifest法理元数据规范  
- [x] Gramine-SGX配置模板  

**Beta｜v10.5-beta-sgx** — SGX-DCAP、MRENCLAVE、Enclave镜像（待落地）  

**Release｜v10.6-canonical** — Zenodo/IPFS 对外存证（按需裁剪，非本内部仓 Release）

---

## 六、Known Limitations

1. Stub模式无硬件信任根  
2. 数据集、统计计算仅占位实现  
3. Hardware Quote 尚未开发（NotImplementedError 为 MVP 预期）  
4. MRENCLAVE 尚未锁定  
5. 不可直接投入生产  

---

## 七、信任边界划分

Enclave：铁律校验、SHA256、Quote调度  
Host：采集、统计、IO、存储  

---

## 八、仓库文件清单

| 文件 | 作用 |
| --- | --- |
| README.md | 宪章与契约 |
| check_isolation.sh | CI 流水线 |
| full_bootstrap.sh | 一键冻结 |
| veto_tee_stub.py | 气闸核心 |
| enclave_entry.py | Enclave IPC 入口 |
| test_iron_laws.py | 回归测试 |
| v105-enclave.manifest.template | Gramine 模板 |
| manifest.json | 基线元数据 |
| yc1_statistics.json | 试点统计 |

---

## BibTeX

```bibtex
@software{huang2026v105research,
  author = {黄清佳},
  title = {v10.5-research: TEE气闸隔离基线},
  year = {2026},
  url = {https://github.com/liu-hui-ming/hundred-crayfish-legion/tree/main/v10.5-research}
}
```
