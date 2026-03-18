"""报告生成Agent — 参考DATAGEN的报告生成模块"""
from agents.base import BaseAgent
from utils.llm import generate_report


REPORT_TEMPLATE = """
# {title}

## 一、摘要
{abstract}

## 二、数据来源与说明
{data_source}

## 三、分析方法
{methodology}

## 四、实验结果与分析
{results}

## 五、主要结论
{conclusions}

## 六、防治建议
{recommendations}

---
*本报告由智慧农业病虫害预警系统自动生成*
"""


class ReportAgent(BaseAgent):
    """报告Agent：自动生成符合比赛要求的研究报告"""
    
    def __init__(self):
        super().__init__(
            name="报告生成Agent",
            description="根据分析结果自动生成结构化研究报告",
        )
    
    def run(self, input_data: dict) -> dict:
        """
        input_data:
        {
            "title": "报告标题",
            "analysis_results": {...},  # 来自DataAgent和PredictAgent的结果
        }
        """
        title = input_data.get("title", "农作物病虫害风险分析报告")
        analysis = input_data.get("analysis_results", {})
        
        # 用AI生成完整报告
        report_content = generate_report(analysis)
        
        return {
            "title": title,
            "content": report_content,
            "format": "markdown",
        }
