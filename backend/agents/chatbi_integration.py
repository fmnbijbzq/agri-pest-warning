"""
集成OpenChatBI — 对话式农业数据分析

OpenChatBI提供:
- NL2SQL: 自然语言→SQL查询
- 自动可视化: Plotly图表
- 对话记忆: 多轮对话上下文
- 时序预测 + 异常检测
"""
import csv
import os
from pathlib import Path
from config.loader import get_active_llm, generate_openchatbi_yaml

_PROJECT_ROOT = Path(__file__).parent.parent
_CATALOG_DIR = _PROJECT_ROOT / "data" / "catalog"

# 预置的表选择示例（避免 BM25 空语料导致 division by zero）
_TABLE_SELECTION_SEEDS = [
    ("查询病虫害历史记录", "pest_history"),
    ("湖南省水稻最常见的病虫害", "pest_history"),
    ("各省份平均风险评分", "pest_history"),
    ("高温高湿条件下的病虫害", "pest_history"),
    ("哪个月份病虫害最多", "pest_history"),
    ("查询病虫害防治知识", "pest_knowledge"),
]


def _ensure_catalog_examples(force=False):
    """确保 catalog 目录有表选择示例，防止 BM25 初始化失败"""
    csv_path = _CATALOG_DIR / "table_selection_example.csv"
    if not force and csv_path.exists() and csv_path.stat().st_size > 50:
        return
    _CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    with open(csv_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["question", "selected_tables"])
        writer.writeheader()
        for question, tables in _TABLE_SELECTION_SEEDS:
            writer.writerow({"question": question, "selected_tables": tables})


def create_chatbi_agent():
    """
    创建OpenChatBI对话Agent

    使用方式:
        graph, config = create_chatbi_agent()
        result = graph.invoke(
            {"messages": [{"role": "user", "content": "湖南水稻最常见的病虫害是什么？"}]},
            config
        )
    """
    try:
        # 从统一配置生成OpenChatBI所需的YAML
        llm = get_active_llm()
        config_file = generate_openchatbi_yaml()
        os.environ["OPENAI_API_KEY"] = llm["api_key"]
        os.environ["OPENAI_API_BASE"] = llm["base_url"]
        os.environ["CONFIG_FILE"] = config_file

        # 确保 catalog 有基础数据
        _ensure_catalog_examples()

        # 加载配置
        import openchatbi
        loader = openchatbi.config
        loader._config = None  # 重置单例，确保使用最新配置
        loader.load(config_file)

        # autoload 可能用空数据覆盖种子文件，重新写入
        _ensure_catalog_examples(force=True)

        # 获取编译好的graph
        graph = openchatbi.get_default_graph()

        config = {"configurable": {"thread_id": "agri-pest-chat"}}

        return graph, config

    except Exception as e:
        print(f"⚠️ OpenChatBI初始化失败: {e}")
        return None, None


def chatbi_query(graph, config, question: str) -> dict:
    """
    使用OpenChatBI执行对话查询

    Returns:
        {"answer": str, "sql": str, "data": list, "chart": object}
    """
    try:
        from langchain_core.messages import HumanMessage

        result = graph.invoke(
            {"messages": [HumanMessage(content=question)]},
            config,
        )

        # 提取结果
        messages = result.get("messages", [])
        answer = ""
        for msg in reversed(messages):
            content = msg.content if hasattr(msg, "content") else str(msg)
            if content and len(content) > 10:
                answer = content
                break

        return {
            "answer": answer,
            "raw": result,
        }
    except Exception as e:
        return {"answer": f"查询失败: {e}", "error": str(e)}


def get_chatbi_or_fallback():
    """
    获取对话引擎：优先OpenChatBI，回退自研DataAgent

    Returns: (agent, engine_type)
    """
    graph, config = create_chatbi_agent()
    if graph is not None:
        return (graph, config), "openchatbi"

    from agents.data_agent import DataAgent
    return DataAgent(), "custom"
