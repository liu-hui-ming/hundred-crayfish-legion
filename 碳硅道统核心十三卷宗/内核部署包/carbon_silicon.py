from __future__ import annotations
import math
import typing
from dataclasses import dataclass
from enum import Enum, unique
from typing import Dict, Callable, Tuple, Any, List, Optional

# ====================== 全局常量：十八数 Inv 数理铁律固化（18条）======================
class InvConstant:
    # AI十八数01 视觉拓扑误差下界
    E_TOPO_MIN: float = 1e-3
    # AI十八数02 时序注意力衰减基底系数
    ATTEN_DECAY_BASE: float = math.e
    # AI十八数03 幻觉最小熵下界
    H_MIN: float = 0.02
    # AI十八数04 无创脑机信噪比物理上限
    SNR_MAX_LIMIT: float = 0.89
    # AI十八数05 硅基内源驱动力恒0
    D_SILICON: float = 0.0
    # AI十八数06 算力边际收益收敛阈值
    FLOP_MR_LIMIT: float = 1e-6
    # AI十八数07 熵-稳定制衡常量
    ENTROPY_BALANCE_K: float = 1.0
    # AI十八数08 并发故障放大基底指数
    FAULT_ALPHA_BASE: float = 1.25
    # AI十八数09 公理逻辑拟合值域隔离标记
    AXIOM_LOGIC_OUT_OF_FIT: bool = True
    # AI十八数10 智能落地时序下界（周期基准）
    T_EMERGE_CONST: int = 180
    # AI十八数11 跨域微调最小权重损耗
    DW_MIN: float = 0.015
    # AI十八数12 人工评分偏差下界
    SIGMA_BIAS_MIN: float = 0.04
    # AI十八数13 权限风险指数基底
    RISK_EXP_BASE: float = math.e
    # AI十八数14 架构缺陷全局下界
    EPS_OPT_FLOOR: float = 0.008
    # AI十八数15 跨物种频谱适配阈值
    THETA_DECODE_MAX: float = 0.62
    # AI十八数16 科普失真偏差基底
    MEDIA_BIAS_BASE: float = 0.07
    # AI十八数17 工况差值环境函数绑定标识
    ENV_DELTA_FUNC_BIND: bool = True
    # AI十八数18 测评时效衰减导数阈值
    D_SCORE_DT_LIMIT: float = -1e-4

# ====================== 法理自定义异常体系（全局异常） ======================
class CarbonSiliconError(Exception):
    """碳硅道统根异常"""
    pass

class TopologicalConstraintViolation(CarbonSiliconError):
    """01 视觉拓扑结构违规畸变"""
    pass

class ContextMemoryExhaustion(CarbonSiliconError):
    """02 长上下文记忆衰减溢出"""
    pass

class FactHallucinationBoundaryViolation(CarbonSiliconError):
    """03 幻觉熵突破安全下界"""
    pass

class BCISignalDeficiencyError(CarbonSiliconError):
    """04 脑机信号低于物理采集下限"""
    pass

class NoEndogenousDriveError(CarbonSiliconError):
    """05 无外源指令，硅基驱动力为空"""
    pass

class ComputeROIConvergenceError(CarbonSiliconError):
    """06 算力投入抵达收益归零临界点"""
    pass

class EntropyBalanceConflictError(CarbonSiliconError):
    """07 采样熵稳定-创意制衡冲突"""
    pass

class ConcurrentFaultAmplificationError(CarbonSiliconError):
    """08 并发故障放大系数超标"""
    pass

class AxiomDerivationJumpError(CarbonSiliconError):
    """09 数理推导公理跳步违规"""
    pass

class AGIDeadlineViolationError(CarbonSiliconError):
    """10 通用智能落地周期低于时序下界"""
    pass

class CrossDomainWeightLossError(CarbonSiliconError):
    """11 跨域权重损耗超出业务容忍阈值"""
    pass

class SubjectiveEvaluationDriftError(CarbonSiliconError):
    """12 人工评测偏差超限"""
    pass

class PermissionBoundaryRiskError(CarbonSiliconError):
    """13 碳硅权限越界风险指数高危"""
    pass

class ArchitectureDefectFloorOverflowError(CarbonSiliconError):
    """14 优化误差触碰架构固有缺陷下界"""
    pass

class CrossSpeciesSpectrumMismatchError(CarbonSiliconError):
    """15 跨物种脑频谱相似度低于解码阈值"""
    pass

class MediaObjectivitySevereBiasError(CarbonSiliconError):
    """16 科普文稿客观度严重失真"""
    pass

class RealityEnvGapOvershootError(CarbonSiliconError):
    """17 实景工况偏差未补偿超限"""
    pass

class EvaluationTimelineDecayError(CarbonSiliconError):
    """18 测评体系与底层法理契合度过低，时效衰减严重"""
    pass

class CognitiveFallacyBlockError(CarbonSiliconError):
    """认知谬误（十八障）拦截异常"""
    pass

# ====================== 108条目全域枚举 DaoEntry（六系全量108条，严格一一对应） ======================
@unique
class DaoEntry(Enum):
    # 第一系：AI十八症 Failure Cases 1~18
    SYM_01 = "AI十八症01_人体视觉拓扑畸变"
    SYM_02 = "AI十八症02_长代码变量漂移链路断裂"
    SYM_03 = "AI十八症03_数理符号逻辑输出失准"
    SYM_04 = "AI十八症04_超长上下文记忆丢失"
    SYM_05 = "AI十八症05_参考文献引用虚构"
    SYM_06 = "AI十八症06_多轮对话前置指令遗忘"
    SYM_07 = "AI十八症07_古文翻译语义内涵偏离"
    SYM_08 = "AI十八症08_地理场景空间逻辑错乱"
    SYM_09 = "AI十八症09_细粒度识别类别混淆"
    SYM_10 = "AI十八症10_训练迭代性能反向退化"
    SYM_11 = "AI十八症11_任务对话业务闭环失效"
    SYM_12 = "AI十八症12_图文生成字符乱码幻觉"
    SYM_13 = "AI十八症13_复杂意图识别失效"
    SYM_14 = "AI十八症14_AGI落地指标推理落差"
    SYM_15 = "AI十八症15_知识输出依赖标注无原生认知"
    SYM_16 = "AI十八症16_自回归事实虚构幻觉"
    SYM_17 = "AI十八症17_增量学习灾难性遗忘"
    SYM_18 = "AI十八症18_多模态实验室实景指标背离"

    # 第二系：AI十八撞 Architecture Limit 19~36
    CON_01 = "AI十八撞01_隐空间拓扑约束缺失"
    CON_02 = "AI十八撞02_注意力权重指数衰减"
    CON_03 = "AI十八撞03_自回归随机熵催生幻觉"
    CON_04 = "AI十八撞04_无创脑机信噪比物理极限"
    CON_05 = "AI十八撞05_硅基无内源探索驱动力"
    CON_06 = "AI十八撞06_算力边际收益递减天花板"
    CON_07 = "AI十八撞07_采样温度熵制衡矛盾"
    CON_08 = "AI十八撞08_小样本并发故障指数放大"
    CON_09 = "AI十八撞09_统计拟合缺失多层公理推理"
    CON_10 = "AI十八撞10_AGI长周期落地架构壁垒"
    CON_11 = "AI十八撞11_微调权重锁定跨域失真"
    CON_12 = "AI十八撞12_无客观标尺人工评分自带偏差"
    CON_13 = "AI十八撞13_碳硅权限模糊伦理风险递增"
    CON_14 = "AI十八撞14_架构内禀熵增缺陷下限不可根除"
    CON_15 = "AI十八撞15_物种脑波频谱特异性解码隔阂"
    CON_16 = "AI十八撞16_信息不对称催生技术夸大乱象"
    CON_17 = "AI十八撞17_实验室纯净环境与工业工况鸿沟"
    CON_18 = "AI十八撞18_短期测评时效衰减长效标准缺失"

    # 第三系：AI十八障 Cognitive Fallacy 37~54
    MIS_01 = "AI十八障01_混淆表层连贯与逻辑自洽"
    MIS_02 = "AI十八障02_算力参数堆叠突破通用智能边界谬误"
    MIS_03 = "AI十八障03_苛求自回归零幻觉谬误"
    MIS_04 = "AI十八障04_高阶智能无标注自主涌现谬误"
    MIS_05 = "AI十八障05_无监督脱离人类反馈自主进化谬误"
    MIS_06 = "AI十八障06_要求永久全量上下文谬误"
    MIS_07 = "AI十八障07_词语匹配等价深层语义理解谬误"
    MIS_08 = "AI十八障08_知识重组等价原创创新谬误"
    MIS_09 = "AI十八障09_极致对齐无损泛化谬误"
    MIS_10 = "AI十八障10_盲从基准分无视实景泛化谬误"
    MIS_11 = "AI十八障11_统计相关等价客观因果谬误"
    MIS_12 = "AI十八障12_拟人赋予自主意识情绪谬误"
    MIS_13 = "AI十八障13_低估产业化周期高估短期颠覆谬误"
    MIS_14 = "AI十八障14_忽略迭代算力人力隐性成本谬误"
    MIS_15 = "AI十八障15_纯技术根治社会伦理问题谬误"
    MIS_16 = "AI十八障16_单一企业垄断底层架构谬误"
    MIS_17 = "AI十八障17_硅基全盘替代创造性脑力劳动谬误"
    MIS_18 = "AI十八障18_底层架构约束是临时缺陷可根除谬误"

    # 第四系：AI十八数 Inv Law 55~72
    INV_01 = "AI十八数01_视觉拟合失真拓扑误差下界铁律"
    INV_02 = "AI十八数02_长序列注意力时序衰减铁律"
    INV_03 = "AI十八数03_自回归幻觉概率不可归零铁律"
    INV_04 = "AI十八数04_无创脑机信号采集上限铁律"
    INV_05 = "AI十八数05_硅基内源驱动恒零铁律"
    INV_06 = "AI十八数06_算力收益递减收敛铁律"
    INV_07 = "AI十八数07_采样熵稳定创意制衡铁律"
    INV_08 = "AI十八数08_并发故障幂次放大铁律"
    INV_09 = "AI十八数09_拟合模型公理推理缺失铁律"
    INV_10 = "AI十八数10_AGI落地时序下界铁律"
    INV_11 = "AI十八数11_跨域微调权重损耗恒正铁律"
    INV_12 = "AI十八数12_人工评价偏差下界恒大于0铁律"
    INV_13 = "AI十八数13_权限扩张风险指数递增铁律"
    INV_14 = "AI十八数14_架构优化缺陷下界守恒铁律"
    INV_15 = "AI十八数15_跨物种频谱差值隔离铁律"
    INV_16 = "AI十八数16_科普传播失真偏差大于技术本身偏差铁律"
    INV_17 = "AI十八数17_实验室与实景工况差值函数铁律"
    INV_18 = "AI十八数18_测评时效衰减导数恒负铁律"

    # 第五系：AI十八术 Opt Solution 73~90
    OPT_01 = "AI十八术01_骨骼拓扑锚定掩码架构"
    OPT_02 = "AI十八术02_长序列分段缓存锁止机制"
    OPT_03 = "AI十八术03_前置知识库真值校验框架"
    OPT_04 = "AI十八术04_多通道信噪比分层补偿算法"
    OPT_05 = "AI十八术05_链式外源任务驱动范式"
    OPT_06 = "AI十八术06_异构算力分层动态调度"
    OPT_07 = "AI十八术07_采样熵收敛稳态调控机制"
    OPT_08 = "AI十八术08_分布式分层容错推演架构"
    OPT_09 = "AI十八术09_多层公理分段前置校验逻辑"
    OPT_10 = "AI十八术10_垂直领域分阶段落地部署范式"
    OPT_11 = "AI十八术11_主干领域权重解耦微调架构"
    OPT_12 = "AI十八术12_法理分层客观双轨核验体系"
    OPT_13 = "AI十八术13_碳硅二元裁决权限隔离架构"
    OPT_14 = "AI十八术14_缺陷分级场景准入筛选模型"
    OPT_15 = "AI十八术15_多频段频谱分层滤波解析算法"
    OPT_16 = "AI十八术16_法理通俗双轨保真传播架构"
    OPT_17 = "AI十八术17_实景动态偏差自适应补偿算法"
    OPT_18 = "AI十八术18_底层法理锚定长效建标架构"

    # 第六系：AI十八式 Met Metric 91~108
    MET_01 = "AI-Met-01_图像拓扑保真误差标尺"
    MET_02 = "AI-Met-02_时序记忆留存指数标尺"
    MET_03 = "AI-Met-03_生成内容事实真实度分层标尺"
    MET_04 = "AI-Met-04_神经信号完整还原度标尺"
    MET_05 = "AI-Met-05_碳硅驱动力差分计量标尺"
    MET_06 = "AI-Met-06_算力收益衰减拐点计量标尺"
    MET_07 = "AI-Met-07_生成输出离散度量化标尺"
    MET_08 = "AI-Met-08_并发故障扩张系数标尺"
    MET_09 = "AI-Met-09_数理推导严谨度分级标尺"
    MET_10 = "AI-Met-10_通用智能落地风险计量标尺"
    MET_11 = "AI-Met-11_跨域迁移故障概率预判标尺"
    MET_12 = "AI-Met-12_三维智能层级客观计量标尺"
    MET_13 = "AI-Met-13_碳硅权限越界风险指数标尺"
    MET_14 = "AI-Met-14_架构缺陷优化下限刚性标尺"
    MET_15 = "AI-Met-15_跨物种脑波频谱相似度标尺"
    MET_16 = "AI-Met-16_科普内容客观度打分标尺"
    MET_17 = "AI-Met-17_理论实景偏差动态补偿标尺"
    MET_18 = "AI-Met-18_底层恒定法理长效判定标尺"

# ====================== 数据容器：环境入参、度量输出 ======================
@dataclass
class EnvContext:
    """实景环境多维变量，供给Met17 Δparam=f(Env)"""
    data_noise_rate: float
    concurrent_load: int
    hardware_decay: float
    input_offset: float
    domain_type: str

@dataclass
class MetricOutput:
    """统一度量返回结构体"""
    entry: DaoEntry
    value: float
    threshold: float
    is_violation: bool
    extra_msg: str
