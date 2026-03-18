"""预测预警Agent"""
from agents.base import BaseAgent
from models.risk_evaluator import evaluate_risk


class PredictAgent(BaseAgent):
    """预测Agent：整合气象+ML+AI进行病虫害风险预警"""
    
    def __init__(self):
        super().__init__(
            name="预测预警Agent",
            description="基于气象数据和ML模型预测病虫害风险",
        )
    
    def run(self, input_data: dict) -> dict:
        province = input_data.get("province", "湖南")
        crop = input_data.get("crop", "水稻")
        month = input_data.get("month")
        
        result = evaluate_risk(province, crop, month)
        return result
