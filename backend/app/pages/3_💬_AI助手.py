"""🤖 AI助手页面 (现代化版本 — 参考 my-smart-farm 聊天界面)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header

inject_css()
page_header(
    "🤖 AI 数据分析助手",
    "用自然语言提问，AI 自动查询数据库并给出分析结果",
    badge="✨ NL2SQL · 智能问答 · 自然语言交互",
)


@st.cache_resource(show_spinner="正在初始化 AI 引擎...")
def init_engine():
    from agents.chatbi_integration import get_chatbi_or_fallback
    return get_chatbi_or_fallback()


if "engine" not in st.session_state:
    st.session_state.engine, st.session_state.engine_type = init_engine()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ── 侧边栏 ──
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1.5rem 0;">'
        '<div style="font-size:2.5rem;">🌾</div>'
        '<div style="font-size:1.1rem;font-weight:700;color:#ecfdf5;margin-top:0.5rem;">智慧农业预警系统</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    engine_tag = "🟢 OpenChatBI" if st.session_state.engine_type == "openchatbi" else "🔵 DataAgent"
    st.markdown(
        f'<div class="engine-badge">{engine_tag}</div>',
        unsafe_allow_html=True,
    )
    st.markdown("")

    if st.button("🗑️ 清空对话", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.85rem;font-weight:700;color:#a7f3d0;margin-bottom:0.8rem;">💡 试试这些问题</div>',
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
        st.markdown(
            f'<div style="font-size:0.8rem;color:#6ee7b7;padding:0.35rem 0.7rem;'
            f'border-left:3px solid rgba(52,211,153,0.4);margin:0.4rem 0;'
            f'background:rgba(52,211,153,0.05);border-radius:0 8px 8px 0;">'
            f'{ex}</div>',
            unsafe_allow_html=True,
        )

# ── 快捷提问按钮 — 参考 my-smart-farm 底部快捷 chip ──
if not st.session_state.chat_history:
    st.markdown(
        '<div style="text-align:center;padding:3rem 0;color:#9ca3af;">'
        '<div style="font-size:3.5rem;margin-bottom:0.8rem;">💬</div>'
        '<div style="font-size:1.05rem;font-weight:600;color:#4b5563;">在下方输入你的问题，开始数据分析</div>'
        '<div style="font-size:0.85rem;margin-top:0.5rem;color:#9ca3af;">AI 将自动查询数据库并生成分析报告</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # 快捷 chip 按钮
    chip_cols = st.columns(3)
    chips = ["湖南省水稻常见病虫害", "各月份风险对比", "高温高湿病虫害排名"]
    for col, chip in zip(chip_cols, chips):
        with col:
            if st.button(chip, use_container_width=True):
                st.session_state.chat_history.append({"role": "user", "content": chip})
                st.rerun()

# ── 对话区域 ──
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("描述你的问题，AI 将自动分析..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("AI 分析中..."):
            try:
                if st.session_state.engine_type == "openchatbi":
                    from agents.chatbi_integration import chatbi_query
                    graph, config = st.session_state.engine
                    result = chatbi_query(graph, config, prompt)
                    response = result.get("answer", "无法获取结果")
                else:
                    result = st.session_state.engine.run({"query": prompt})
                    if "error" in result:
                        response = f"❌ {result['error']}"
                    else:
                        response = (
                            f"**SQL 查询**:\n```sql\n{result['sql']}\n```\n\n"
                            f"**分析结果**:\n{result['interpretation']}"
                        )
            except Exception as e:
                response = f"⚠️ 出错: {str(e)}\n\n请确保已配置 API Key 并初始化数据库"

        st.markdown(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})
