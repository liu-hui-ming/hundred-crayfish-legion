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

# =========【移位至此！原先写在枚举前面，此处修正后消除NameError】=========
# 十八症条目-专属异常一对一映射（修复缺陷2：异常张冠李戴）
SYM_EXCEPTION_MAP: Dict = {
    DaoEntry.SYM_01: TopologicalConstraintViolation,
    DaoEntry.SYM_02: ContextMemoryExhaustion,
    DaoEntry.SYM_03: FactHallucinationBoundaryViolation,
    DaoEntry.SYM_04: ContextMemoryExhaustion,
    DaoEntry.SYM_05: MediaObjectivitySevereBiasError,
    DaoEntry.SYM_06: ContextMemoryExhaustion,
    DaoEntry.SYM_07: SubjectiveEvaluationDriftError,
    DaoEntry.SYM_08: CrossSpeciesSpectrumMismatchError,
    DaoEntry.SYM_09: ConcurrentFaultAmplificationError,
    DaoEntry.SYM_10: ArchitectureDefectFloorOverflowError,
    DaoEntry.SYM_11: PermissionBoundaryRiskError,
    DaoEntry.SYM_12: FactHallucinationBoundaryViolation,
    DaoEntry.SYM_13: AxiomDerivationJumpError,
    DaoEntry.SYM_14: AGIDeadlineViolationError,
    DaoEntry.SYM_15: NoEndogenousDriveError,
    DaoEntry.SYM_16: FactHallucinationBoundaryViolation,
    DaoEntry.SYM_17: ComputeROIConvergenceError,
    DaoEntry.SYM_18: RealityEnvGapOvershootError,
}

# ====================== 数据容器：环境入参、度量输出 ======================
@dataclass
class EnvContext:
    """实景环境多维变量，供给Met17 Δparam=f(Env)"""
    data_noise_rate: float
    concurrent_load: int
    hardware_decay: float
    input_offset: float
    domain_type: str  # 定义预留，后续OPT拓展使用

@dataclass
class MetricOutput:
    """统一度量返回结构体"""
    entry: DaoEntry
    value: float
    threshold: float
    is_violation: bool
    extra_msg: str

# ====================== 核心算子实现（强制重点：Met17、Met18） ======================
class CoreMetricOperator:
    def __init__(self):
        self.inv = InvConstant

    # Met-17 Δ_param = f(Env) 实景偏差补偿函数
    def calc_env_delta(self, env: EnvContext) -> float:
        """工况差值原生函数"""
        base = (env.data_noise_rate * 0.35) + (env.concurrent_load / 10000 * 0.4) + (env.hardware_decay * 0.15) + (env.input_offset * 0.1)
        return max(base, 0.0)

    def dynamic_compensate(self, env: EnvContext, raw_param: float) -> float:
        """AI-Opt17自适应补偿，分段动态权重上调"""
        delta = self.calc_env_delta(env)
        if delta < 0.1:
            comp = delta * 0.8
        elif delta < 0.3:
            comp = delta * 1.2
        else:
            comp = delta * 1.8  #极端环境上调补偿权重
        return raw_param + comp

    # Met-18 S_inv 长效法理契合打分 + dScore/dt导数监测
    def calc_s_invariant(self, rule_match_count: int, total_rule: int, time_decay_coeff: float) -> float:
        """底层法理贴合度 S_inv ∈ [0,1]"""
        base = rule_match_count / total_rule
        decay_penalty = abs(min(time_decay_coeff, 0.0))
        s = max(base - decay_penalty, 0.0)
        return s

    def eval_score_derivative(self, score_t1: float, score_t2: float, delta_t: float) -> float:
        """dScore/dt，监测时效衰减 ∂Score/∂t <0"""
        if delta_t == 0:
            return 0.0
        deriv = (score_t2 - score_t1) / delta_t
        return deriv

# ====================== 全域六系校验路由器（单核分发核心） ======================
class DaoRouter:
    def __init__(self):
        self.operator = CoreMetricOperator()
        # 路由注册表：DaoEntry -> 校验处理函数
        self.route_map: Dict[DaoEntry, Callable] = self._build_full_route_table()

    def _build_full_route_table(self) -> Dict[DaoEntry, Callable]:
        """全量108条目路由绑定，六系分支一一映射"""
        route = {}
        # 1.十八症 SYM 故障检测分支
        for entry in [DaoEntry.SYM_01,DaoEntry.SYM_02,DaoEntry.SYM_03,DaoEntry.SYM_04,DaoEntry.SYM_05,
                      DaoEntry.SYM_06,DaoEntry.SYM_07,DaoEntry.SYM_08,DaoEntry.SYM_09,DaoEntry.SYM_10,
                      DaoEntry.SYM_11,DaoEntry.SYM_12,DaoEntry.SYM_13,DaoEntry.SYM_14,DaoEntry.SYM_15,
                      DaoEntry.SYM_16,DaoEntry.SYM_17,DaoEntry.SYM_18]:
            route[entry] = self._sym_check
        # 2.十八撞 CON 架构常量约束分支
        for entry in [DaoEntry.CON_01,DaoEntry.CON_02,DaoEntry.CON_03,DaoEntry.CON_04,DaoEntry.CON_05,
                      DaoEntry.CON_06,DaoEntry.CON_07,DaoEntry.CON_08,DaoEntry.CON_09,DaoEntry.CON_10,
                      DaoEntry.CON_11,DaoEntry.CON_12,DaoEntry.CON_13,DaoEntry.CON_14,DaoEntry.CON_15,
                      DaoEntry.CON_16,DaoEntry.CON_17,DaoEntry.CON_18]:
            route[entry] = self._con_constraint_check
        #3.十八障 MIS 认知谬误阻断分支
        for entry in [DaoEntry.MIS_01,DaoEntry.MIS_02,DaoEntry.MIS_03,DaoEntry.MIS_04,DaoEntry.MIS_05,
                      DaoEntry.MIS_06,DaoEntry.MIS_07,DaoEntry.MIS_08,DaoEntry.MIS_09,DaoEntry.MIS_10,
                      DaoEntry.MIS_11,DaoEntry.MIS_12,DaoEntry.MIS_13,DaoEntry.MIS_14,DaoEntry.MIS_15,
                      DaoEntry.MIS_16,DaoEntry.MIS_17,DaoEntry.MIS_18]:
            route[entry] = self._mis_cognitive_block
        #4.十八数 INV 数理只读校验分支
        for entry in [DaoEntry.INV_01,DaoEntry.INV_02,DaoEntry.INV_03,DaoEntry.INV_04,DaoEntry.INV_05,
                      DaoEntry.INV_06,DaoEntry.INV_07,DaoEntry.INV_08,DaoEntry.INV_09,DaoEntry.INV_10,
                      DaoEntry.INV_11,DaoEntry.INV_12,DaoEntry.INV_13,DaoEntry.INV_14,DaoEntry.INV_15,
                      DaoEntry.INV_16,DaoEntry.INV_17,DaoEntry.INV_18]:
            route[entry] = self._inv_math_check
        #5.十八术 OPT 算子强制调用分支
        for entry in [DaoEntry.OPT_01,DaoEntry.OPT_02,DaoEntry.OPT_03,DaoEntry.OPT_04,DaoEntry.OPT_05,
                      DaoEntry.OPT_06,DaoEntry.OPT_07,DaoEntry.OPT_08,DaoEntry.OPT_09,DaoEntry.OPT_10,
                      DaoEntry.OPT_11,DaoEntry.OPT_12,DaoEntry.OPT_13,DaoEntry.OPT_14,DaoEntry.OPT_15,
                      DaoEntry.OPT_16,DaoEntry.OPT_17,DaoEntry.OPT_18]:
            route[entry] = self._opt_operator_invoke
        #6.十八式 MET 度量打分输出分支
        for entry in [DaoEntry.MET_01,DaoEntry.MET_02,DaoEntry.MET_03,DaoEntry.MET_04,DaoEntry.MET_05,
                      DaoEntry.MET_06,DaoEntry.MET_07,DaoEntry.MET_08,DaoEntry.MET_09,DaoEntry.MET_10,
                      DaoEntry.MET_11,DaoEntry.MET_12,DaoEntry.MET_13,DaoEntry.MET_14,DaoEntry.MET_15,
                      DaoEntry.MET_16,DaoEntry.MET_17,DaoEntry.MET_18]:
            route[entry] = self._met_metric_calc
        return route

    # 六系对应处理逻辑
    def _sym_check(self, entry: DaoEntry, raw_val: float) -> MetricOutput:
        """故障实例检测，违规抛对应异常"""
        thresh_map = {
            DaoEntry.SYM_01: InvConstant.E_TOPO_MIN,
            DaoEntry.SYM_04: 0.2
        }
        thresh = thresh_map.get(entry, 0.1)
        # SYM_04：记忆留存过低触发；其余：指标超阈触发
        violate = (raw_val < thresh) if entry == DaoEntry.SYM_04 else (raw_val > thresh)
        if violate:
            if entry == DaoEntry.SYM_01:
                raise TopologicalConstraintViolation(f"{entry.value} 拓扑误差超限")
            if entry == DaoEntry.SYM_04:
                raise ContextMemoryExhaustion(f"{entry.value} 记忆留存过低")
            # 其余症条目：按一对一异常映射抛出
            raise SYM_EXCEPTION_MAP.get(entry, CarbonSiliconError)(f"{entry.value} 故障超限")
        return MetricOutput(entry, raw_val, thresh, violate, "故障检测完成")

    def _con_constraint_check(self, entry: DaoEntry, raw_val: float) -> MetricOutput:
        """架构底层约束常量校验"""
        violate = raw_val < 0
        if violate:
            raise ArchitectureDefectFloorOverflowError(f"{entry.value}触碰架构约束边界")
        return MetricOutput(entry, raw_val, 0, violate, "架构约束校验通过")

    def _mis_cognitive_block(self, entry: DaoEntry, raw_val: float) -> MetricOutput:
        """认知谬误拦截，命中直接阻断"""
        if raw_val > 0.5:
            raise CognitiveFallacyBlockError(f"触发{entry.value}认知谬误，操作拦截")
        return MetricOutput(entry, raw_val, 0.5, False, "无认知谬误")

    def _inv_math_check(self, entry: DaoEntry, raw_val: float) -> MetricOutput:
        """十八数数理铁律只读校验，不可突破下界"""
        min_map = {
            DaoEntry.INV_01: InvConstant.E_TOPO_MIN,
            DaoEntry.INV_03: InvConstant.H_MIN
        }
        floor = min_map.get(entry, 1e-3)
        violate = raw_val < floor
        if violate:
            raise FactHallucinationBoundaryViolation(f"{entry.value}突破数理下界")
        return MetricOutput(entry, raw_val, floor, violate, "数理铁律校验合规")

    def _opt_operator_invoke(self, entry: DaoEntry, env: Optional[EnvContext] = None, raw_param: float = 0.0) -> MetricOutput:
        """十八术优化算子强制执行，重点绑定OPT17/18"""
        val = raw_param
        if entry == DaoEntry.OPT_17 and env is not None:
            val = self.operator.dynamic_compensate(env, raw_param)
        return MetricOutput(entry, val, raw_param, False, "优化算子执行完成")

    def _met_metric_calc(self, entry: DaoEntry, **kwargs) -> MetricOutput:
        """十八式度量标尺计算，MET17、MET18专属逻辑"""
        if entry == DaoEntry.MET_17:
            env: EnvContext = kwargs["env"]
            raw = kwargs["raw"]
            comp_val = self.operator.dynamic_compensate(env, raw)
            return MetricOutput(entry, comp_val, raw, comp_val-raw>0.2, "工况补偿计算完成")
        if entry == DaoEntry.MET_18:
            match_cnt = kwargs["match"]
            total = kwargs["total"]
            decay = kwargs["decay"]
            s_inv = self.operator.calc_s_invariant(match_cnt, total, decay)
            deriv = self.operator.eval_score_derivative(kwargs["t1"], kwargs["t2"], kwargs["dt"])
            violate = s_inv < 0.6 or deriv < InvConstant.D_SCORE_DT_LIMIT
            if violate:
                raise EvaluationTimelineDecayError(f"S_inv={s_inv:.3f},时效衰减导数{deriv:.5f}")
            return MetricOutput(entry, s_inv, 0.6, violate, f"长效契合度，导数={deriv:.5f}")
        #其余16条度量通用计算占位
        return MetricOutput(entry, kwargs.get("val",0.0),0.1,False,"常规度量计算")

    # 统一入口：单核全域调度唯一暴露接口
    def dispatch(self, entry: DaoEntry, **kwargs) -> MetricOutput:
        if entry not in self.route_map:
            raise CarbonSiliconError(f"DaoEntry {entry} 未注册，108条目缺失")
        handler = self.route_map[entry]
        return handler(entry,**kwargs)

# ====================== 全局单例导出（单核唯一驱动） ======================
carbon_silicon_kernel = DaoRouter()
