from __future__ import annotations

# 碳硅同盟铁律体系：权威 1–12 层（L1 至 L12 为完整闭环，不可再增删层级编号）
# L1–L8：铁律/数据/发布/集群/时序/组网/确权；L9–L12：商业生态/运营/交付/超维意识（终态全谱系）
ALLIANCE_LAYER_COUNT = 12

# 每一项：layer(1~12), key, name, summary
ALLIANCE_12_LAYERS: tuple[dict, ...] = (
    {
        "layer": 1,
        "key": "rule_law",
        "name": "规则铁律层",
        "summary": "内容质检、合规校验、分级评级",
    },
    {
        "layer": 2,
        "key": "security_permission",
        "name": "安全权限层",
        "summary": "鉴权管控、日志脱敏、风险防护",
    },
    {
        "layer": 3,
        "key": "data_autonomy",
        "name": "数据自治层",
        "summary": "冷热归档、自动运维、日志管理",
    },
    {
        "layer": 4,
        "key": "dispatch_publish",
        "name": "发布调度层",
        "summary": "队列调度、多渠道分发、异常重试",
    },
    {
        "layer": 5,
        "key": "cluster_hyper",
        "name": "集群超维层",
        "summary": "负载均衡、灰度发布、动态风控",
    },
    {
        "layer": 6,
        "key": "time_series_heal",
        "name": "时序自愈层",
        "summary": "风险推演、故障溯源、自主修复",
    },
    {
        "layer": 7,
        "key": "crypto_mesh",
        "name": "加密组网层",
        "summary": "硬件绑定、离线授权、分布式互联",
    },
    {
        "layer": 8,
        "key": "attest_eternal",
        "name": "确权永生层",
        "summary": "全域存证、不可篡改、星际同步、系统永生",
    },
    {
        "layer": 9,
        "key": "commercial_ecosystem",
        "name": "商业生态层",
        "summary": "发卡、知识/合规文档、品牌开屏等对外商业触点与生态位",
    },
    {
        "layer": 10,
        "key": "ops_closed_loop",
        "name": "运营闭环层",
        "summary": "产品更新、权限/授权策略、多渠道告警与处置闭环",
    },
    {
        "layer": 11,
        "key": "visual_delivery",
        "name": "可视化交付层",
        "summary": "Web 管理后台、EXE 等离线/边缘交付形态、可视运维",
    },
    {
        "layer": 12,
        "key": "hyperdimensional_conscious",
        "name": "超维意识自治层",
        "summary": "分布式 AI 自治中枢：战略推演、任务自编排、跨节点意识协同、时序命运预判、内生决策闭环",
    },
)

assert len(ALLIANCE_12_LAYERS) == ALLIANCE_LAYER_COUNT, "12 层定义必须与 ALLIANCE_LAYER_COUNT 一致"


def get_layer_by_id(layer: int) -> dict | None:
    if 1 <= layer <= ALLIANCE_LAYER_COUNT:
        return next((x for x in ALLIANCE_12_LAYERS if x["layer"] == layer), None)
    return None


def layers_to_public_dicts() -> list[dict[str, int | str]]:
    return [dict(x) for x in ALLIANCE_12_LAYERS]
