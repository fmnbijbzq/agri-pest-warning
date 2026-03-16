"""AI助手页面 (v3.0 专业级 UI)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header, svg_icon, sidebar_brand, sidebar_footer

inject_css()
page_header(
    "AI 数据分析助手",
    "用自然语言提问，AI 自动查询数据库并给出分析结果",
    badge="NL2SQL · 智能问答 · 自然语言交互",
    icon="bot",
)


@st.cache_resource(show_spinner="正在初始化 AI 引擎...")
def init_engine():
    from agents.chatbi_integration import get_chatbi_or_fallback
    return get_chatbi_or_fallback()


def _query_ai(question: str) -> str:
    """调用 AI 引擎获取回复"""
    try:
        if st.session_state.engine_type == "openchatbi":
            from agents.chatbi_integration import chatbi_query
            graph, config = st.session_state.engine
            result = chatbi_query(graph, config, question)
            return result.get("answer", "无法获取结果")
        else:
            result = st.session_state.engine.run({"query": question})
            if "error" in result:
                return f"**Error:** {result['error']}"
            return (
                f"**SQL 查询**:\n```sql\n{result['sql']}\n```\n\n"
                f"**分析结果**:\n{result['interpretation']}"
            )
    except Exception as e:
        return f"出错: {str(e)}\n\n请确保已配置 API Key 并初始化数据库"


if "engine" not in st.session_state:
    st.session_state.engine, st.session_state.engine_type = init_engine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── 侧边栏 ──
with st.sidebar:
    sidebar_brand()

    engine_tag = "OpenChatBI" if st.session_state.engine_type == "openchatbi" else "DataAgent"
    st.markdown(
        f'<div class="engine-badge" style="display:flex;align-items:center;justify-content:center;gap:0.4rem;">'
        f'{svg_icon("cpu", 15, "#6ee7b7")}{engine_tag}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    if st.button("清空对话", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.pop("pending_prompt", None)
        st.rerun()

    st.markdown("---")
    st.markdown(
        f'<div style="font-size:0.82rem;font-weight:600;color:#a7f3d0;margin-bottom:0.6rem;'
        f'display:flex;align-items:center;gap:0.35rem;">'
        f'{svg_icon("lightbulb", 14, "#a7f3d0")}试试这些问题</div>',
        unsafe_allow_html=True,
    )
    examples = [
        "湖南省水稻最常见的病虫害？",
        "哪个月份病虫害最频繁？",
        "高湿度下哪些病虫害风险最高？",
        "对比各省份平均风险评分",
        "温度超过30度时严重程度分布？",
    ]
    for ex in examples:
        st.markdown(f'<div class="example-q">{ex}</div>', unsafe_allow_html=True)

    sidebar_footer()

# ── 快捷提问按钮 ──
if not st.session_state.chat_history:
    st.markdown(
        f'<div class="empty-state">'
        f'<div class="empty-icon">{svg_icon("message-circle", 28, "#34d399")}</div>'
        f'<div class="empty-title">在下方输入你的问题，开始数据分析</div>'
        f'<div class="empty-desc">AI 将自动查询数据库并生成分析报告</div>'
        f'</div>',
        unsafe_allow_html=True,
    )

    chip_cols = st.columns(3)
    chips = ["湖南省水稻常见病虫害", "各月份风险对比", "高温高湿病虫害排名"]
    for col, chip in zip(chip_cols, chips):
        with col:
            if st.button(chip, use_container_width=True):
                st.session_state.pending_prompt = chip
                st.rerun()

# ── 对话区域 ──
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── 处理待回答的问题（来自 chip 按钮或 chat_input）──
pending = st.session_state.pop("pending_prompt", None)
prompt = st.chat_input("描述你的问题，AI 将自动分析...")

if prompt:
    pending = prompt

if pending:
    st.session_state.chat_history.append({"role": "user", "content": pending})
    with st.chat_message("user"):
        st.markdown(pending)

    with st.chat_message("assistant"):
        with st.spinner("AI 分析中..."):
            response = _query_ai(pending)
        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
