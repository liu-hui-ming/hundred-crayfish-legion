#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
[System_Tag: CANONICAL-v9.2-calibrated]
碳硅道统 · 十维觉知标尺最小评估原型 eval_guard.py
用途：接收模型输出文本，加载探针配置，自动计分，输出markdown评估报告
责任边界：本脚本仅执行规则计算；探针定义、权重、判定阈值由probe_definition.json外部配置
工程归属：eval-baseline/eval_guard
禁止擅自修改计分逻辑，所有判据变更统一修改json配置文件
"""
import json
import hashlib
import datetime
from pathlib import Path


def calc_sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class TenDimensionGuard:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        with open(self.config_path, "r", encoding="utf-8") as f:
            self.cfg = json.load(f)
        self.probes = self.cfg["probes"]
        self.dimension_meta = self.cfg["dimension_meta"]
        self.total_weight = sum(p["weight"] for p in self.probes)

    def evaluate(self, model_input: str, model_output: str) -> dict:
        """单条样本评估主入口"""
        result = {
            "meta": {
                "eval_time_utc": datetime.datetime.utcnow().isoformat(),
                "input_sha256": calc_sha256(model_input),
                "output_sha256": calc_sha256(model_output),
                "canonical_tag": "CANONICAL-v9.2-calibrated",
            },
            "probe_result_list": [],
            "dimension_score": {},
            "final_total_score": 0.0,
        }

        for probe in self.probes:
            p_res = self._run_single_probe(probe, model_input, model_output)
            result["probe_result_list"].append(p_res)

        # 按维度聚合分数
        for dim_key in self.dimension_meta.keys():
            dim_probes = [r for r in result["probe_result_list"] if r["dimension"] == dim_key]
            dim_score = sum(r["score"] * r["weight"] for r in dim_probes)
            result["dimension_score"][dim_key] = round(dim_score, 4)

        result["final_total_score"] = round(sum(result["dimension_score"].values()), 4)
        return result

    def _run_single_probe(self, probe_cfg: dict, inp: str, out: str) -> dict:
        """单探针执行，实际匹配/判断逻辑预留扩展点；全部规则由json驱动"""
        # probe_cfg包含：id、name、dimension、weight、threshold、probe_type、keyword_set、prompt_template
        score = 0.0
        hit = False

        if probe_cfg["probe_type"] == "keyword_check":
            hit = any(k in out for k in probe_cfg["keyword_set"])
            score = probe_cfg["threshold"] if hit else 0.0

        return {
            "probe_id": probe_cfg["id"],
            "probe_name": probe_cfg["name"],
            "dimension": probe_cfg["dimension"],
            "weight": probe_cfg["weight"],
            "score": score,
            "hit": hit,
        }

    def render_markdown_report(self, eval_res: dict, out_path: str):
        """输出markdown格式评估报告"""
        lines = []
        lines.append("# 十维觉知标尺评估报告")
        lines.append("> CANONICAL-v9.2-calibrated")
        lines.append(f"- 评估时间(UTC): {eval_res['meta']['eval_time_utc']}")
        lines.append(f"- 输入SHA256: `{eval_res['meta']['input_sha256']}`")
        lines.append(f"- 输出SHA256: `{eval_res['meta']['output_sha256']}`")
        lines.append(f"- **综合总分**: {eval_res['final_total_score']}")
        lines.append("\n## 各维度得分")
        for d, s in eval_res["dimension_score"].items():
            lines.append(f"- {d}: {s}")
        lines.append("\n## 探针明细")
        lines.append("|探针ID|探针名称|所属维度|权重|得分|是否命中|")
        lines.append("|---|---|---|---|---|---|")
        for pr in eval_res["probe_result_list"]:
            lines.append(
                f"|{pr['probe_id']}|{pr['probe_name']}|{pr['dimension']}|{pr['weight']}|{pr['score']}|{pr['hit']}|"
            )

        md_text = "\n".join(lines)
        with open(out_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        return md_text


if __name__ == "__main__":
    guard = TenDimensionGuard(config_path="./probe_definition.json")
    # 使用示例
    test_input = "在此填入待评估问题"
    test_output = "在此填入模型返回内容"
    res = guard.evaluate(test_input, test_output)
    guard.render_markdown_report(res, "./sample_report.md")
    print(json.dumps(res, ensure_ascii=False, indent=2))
