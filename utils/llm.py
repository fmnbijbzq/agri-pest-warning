"""大模型调用封装 — 支持DeepSeek和通用OpenAI兼容接口，一键切换"""
from openai import OpenAI
from config.settings import (
    LLM_PROVIDER,
    DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL,
    OPENAI_COMPATIBLE_BASE_URL, OPENAI_COMPATIBLE_API_KEY, OPENAI_COMPATIBLE_MODEL,
)


def get_llm_client() -> tuple[OpenAI, str]:
    """获取LLM客户端和模型名称，返回 (client, model_name)"""
    if LLM_PROVIDER == "deepseek":
        client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)
        return client, DEEPSEEK_MODEL
    elif LLM_PROVIDER == "openai_compatible":
        if not OPENAI_COMPATIBLE_BASE_URL or not OPENAI_COMPATIBLE_API_KEY or not OPENAI_COMPATIBLE_MODEL:
            raise ValueError(
                "使用 openai_compatible 时，必须设置 OPENAI_COMPATIBLE_BASE_URL、"
                "OPENAI_COMPATIBLE_API_KEY、OPENAI_COMPATIBLE_MODEL"
            )
        client = OpenAI(api_key=OPENAI_COMPATIBLE_API_KEY, base_url=OPENAI_COMPATIBLE_BASE_URL)
        return client, OPENAI_COMPATIBLE_MODEL
    else:
        raise ValueError(f"不支持的LLM提供商: {LLM_PROVIDER}")


def chat(prompt: str, system: str = "你是一个农业病虫害防治专家。", temperature: float = 0.7) -> str:
    """简易对话接口"""
    client, model = get_llm_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
    )
    return response.choices[0].message.content


def chat_with_data(query: str, data_context: str) -> str:
    """带数据上下文的对话 — 用于数据分析Agent"""
    system = (
        "你是一个专业的农业大数据分析师，擅长分析气象数据和病虫害数据。\n"
        "请基于以下数据回答用户的问题，用中文回答，给出具体的数据支撑和分析结论。\n"
        f"\n【数据上下文】\n{data_context}"
    )
    return chat(query, system=system, temperature=0.3)


def generate_report(analysis_results: dict) -> str:
    """生成研究报告 — 用于报告生成Agent"""
    system = (
        "你是一个农业大数据研究报告撰写专家。\n"
        "请根据提供的分析结果，撰写一份结构化的研究报告，包含以下部分：\n"
        "1. 摘要\n2. 数据来源与说明\n3. 分析方法\n4. 实验结果\n5. 主要结论\n6. 防治建议\n"
        "使用专业但易懂的语言，适合学术场景。"
    )
    prompt = f"分析结果数据：\n{analysis_results}"
    return chat(prompt, system=system, temperature=0.5)
