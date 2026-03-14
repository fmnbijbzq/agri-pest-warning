"""
集成DATAGEN — 多Agent研究助手（自动分析+报告生成）

DATAGEN架构:
  Hypothesis → Process → [Coder/Search/Visualization/Report] → QualityReview → NoteTaker → 循环

我们的用法:
  传入农业分析数据 → DATAGEN多Agent自动分析 → 输出研究报告
"""
import os
import sys
from pathlib import Path
from config.loader import get_active_llm, generate_datagen_yaml

# DATAGEN路径
DATAGEN_PATH = Path(__file__).parent.parent / "external" / "DATAGEN"
PROJECT_ROOT = Path(__file__).parent.parent


def _setup_datagen_env():
    """配置DATAGEN所需的环境变量（根据统一配置自动选择LLM提供商）"""
    llm = get_active_llm()
    os.environ["OPENAI_API_KEY"] = llm["api_key"]
    os.environ["OPENAI_API_BASE"] = llm["base_url"]
    os.environ["WORKING_DIRECTORY"] = str(PROJECT_ROOT / "data" / "datagen_workspace")

    # 确保工作目录存在
    Path(os.environ["WORKING_DIRECTORY"]).mkdir(parents=True, exist_ok=True)


def _add_datagen_to_path():
    """将DATAGEN添加到Python路径"""
    if str(DATAGEN_PATH) not in sys.path:
        sys.path.insert(0, str(DATAGEN_PATH))


def create_datagen_workflow():
    """
    创建DATAGEN工作流实例
    
    返回编译好的LangGraph workflow，可以直接调用
    """
    if not DATAGEN_PATH.exists():
        raise FileNotFoundError(
            f"DATAGEN未克隆到 {DATAGEN_PATH}\n"
            f"请运行: git clone https://github.com/starpig1129/DATAGEN.git {DATAGEN_PATH}"
        )
    
    _setup_datagen_env()
    _add_datagen_to_path()
    
    # 从统一配置生成DATAGEN所需的agents YAML
    custom_config = generate_datagen_yaml()
    os.environ["AGENT_MODELS_CONFIG"] = custom_config
    
    from src.core.language_models import LanguageModelManager
    from src.core.workflow import WorkflowManager
    
    lm_manager = LanguageModelManager(config_path=custom_config)
    working_dir = os.environ["WORKING_DIRECTORY"]
    
    workflow_manager = WorkflowManager(lm_manager, working_dir)
    return workflow_manager.get_graph()


def run_datagen_analysis(research_topic: str) -> str:
    """
    使用DATAGEN完整pipeline运行分析
    
    Args:
        research_topic: 研究主题描述
        
    Returns:
        生成的研究报告（Markdown格式）
    """
    try:
        graph = create_datagen_workflow()
        
        # DATAGEN的输入格式
        initial_state = {
            "messages": [{"role": "user", "content": research_topic}],
            "team_members": ["Hypothesis", "Process", "Visualization", 
                           "Search", "Coder", "Report", "QualityReview"],
        }
        
        config = {"configurable": {"thread_id": "agri-pest-analysis"}}
        
        # 运行workflow
        result = graph.invoke(initial_state, config)
        
        # 提取报告内容
        if "messages" in result:
            messages = result["messages"]
            # 找最后一条报告相关的消息
            for msg in reversed(messages):
                content = msg.get("content", "") if isinstance(msg, dict) else str(msg)
                if len(content) > 200:  # 报告通常较长
                    return content
        
        return str(result)
        
    except Exception as e:
        print(f"⚠️ DATAGEN运行失败: {e}")
        print("   回退到自研报告生成方案")
        return None


def generate_research_report(analysis_data: dict) -> str:
    """
    生成研究报告 — 优先DATAGEN，回退自研
    
    Args:
        analysis_data: 分析结果数据字典
    """
    # 构造研究主题描述
    topic = (
        f"请基于以下农业病虫害分析数据，撰写一份完整的研究报告：\n\n"
        f"研究标题: {analysis_data.get('title', '农作物病虫害风险分析')}\n"
        f"分析作物: {analysis_data.get('crop', '未知')}\n"
        f"分析区域: {analysis_data.get('provinces', [])}\n"
        f"数据年份: {analysis_data.get('year_range', '')}\n"
        f"总记录数: {analysis_data.get('total_records', 0)}\n"
        f"平均风险评分: {analysis_data.get('avg_risk', 0)}\n"
        f"高发病虫害: {analysis_data.get('top_pests', {})}\n"
        f"严重程度分布: {analysis_data.get('severity_dist', {})}\n"
        f"月度风险趋势: {analysis_data.get('monthly_risk', {})}\n"
        f"气象概况: {analysis_data.get('weather_summary', {})}\n\n"
        f"报告要求：\n"
        f"1. 包含摘要、数据来源、分析方法、实验结果、主要结论、防治建议\n"
        f"2. 语言专业严谨，适合学术场景\n"
        f"3. 结论要有具体数据支撑\n"
    )
    
    # 尝试使用DATAGEN
    if DATAGEN_PATH.exists():
        try:
            report = run_datagen_analysis(topic)
            if report:
                return report
        except Exception as e:
            print(f"DATAGEN失败: {e}")
    
    # 回退到自研方案
    from utils.llm import generate_report
    return generate_report(analysis_data)
