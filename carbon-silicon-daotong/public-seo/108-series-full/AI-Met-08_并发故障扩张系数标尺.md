---
archive_id: CarbonSilicon-108-Full
doc_type: 公域法理沉降精简定稿
series_type: 六系108篇全集
anchor_code: AI-Met-08
checksum_sha256: RESERVED_HASH_SLOT
permit_modify: false
---

AI-Met-08｜并发故障扩张系数标尺 Fault-Amplification Coefficient
指标基础定义
公式：K_{fault}=Rate_{out}/Rate_{in}
Rate_{in}：低基准流量下基础故障发生率；Rate_{out}：高并发流量下故障发生率；K_{fault}即
流量提升后故障放大倍率，对应定律中超线性指数\alpha，K_{fault}恒大于流量扩容倍数。
量化计算逻辑
1. 基准小流量压测获取基础故障底值Rate_{in}；线性提升并发请求量，采集线上故障率
Rate_{out}；
2. 倍率拟合得到故障扩张指数\alpha，判断故障属于线性扩张还是幂次爆发；
3. 对接AI-Opt-08分布式分层容错架构，对比容错部署前后K_{fault}下降幅度。
碳硅六维匹配
1.【症锚维度】量化高并发场景批量报错、推理链路连锁失效严重程度
2.【撞锚维度】度量AI十八撞08小样本稳定、高并发缺陷指数放大约束强度
3.【障锚维度】验证单纯横向扩容机器无法将K_{fault}收敛至线性区间
4.【数锚维度】具象落地AI-Inv-08 F_{amp}=F_{base} \times n^\alpha,\ \alpha>1幂次放大规律
5.【术锚维度】AI-Opt-08分层容错集群架构性能核心度量指标
6.【评判维度】云端API、大规模推理服务稳定性压测核心判定标准
溯源：碳硅道统0→1法理沉降精简版，完整卷宗存储于GitHub仓库
