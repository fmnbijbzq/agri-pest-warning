"""智慧农业病虫害预警系统 — 主页 (现代化版本)"""
import streamlit as st
from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="首页 - 智慧农业预警",
    page_icon="🏠",
    layout="wide",
)

from app.ui_style import inject_css, page_header, feature_card, feature_card_row, stat_card, stat_card_row, section

inject_css()

# ── Hero ──
page_header(
    "🌾 智慧农业病虫害预警系统",
    "基于大数据分析与 AI Agent 技术，为农业工作者提供病虫害智能预警和防治建议",
    badge="✨ AI 驱动 · 数据赋能 · 精准防治",
)

# ── 快速统计 ──
db_path = ROOT / "data" / "agri_pest.db"
if db_path.exists():
    from utils.database import execute_query
    try:
        overview = execute_query(
            "SELECT COUNT(*) as cnt, COUNT(DISTINCT province) as prov, "
            "COUNT(DISTINCT crop) as crop, ROUND(AVG(risk_score),3) as avg_risk "
            "FROM pest_history"
        )
        row = overview.iloc[0]

        section("核心数据指标", "📈")

        stat_card_row([
            ("📋", f"{int(row['cnt']):,}", "数据总量", "条历史记录"),
            ("🗺️", str(int(row['prov'])), "覆盖省份", "个监测区域"),
            ("🌱", str(int(row['crop'])), "作物种类", "种主要作物"),
            ("⚡", f"{row['avg_risk']:.1%}", "平均风险", "全局风险均值"),
        ])
    except Exception:
        pass

st.markdown("")

# ── 功能模块 ──
section("功能模块", "🚀")

modules = [
    ("📊", "数据总览", "历史病虫害数据多维度可视化，支持省份、作物交叉筛选分析", "Plotly + Pandas", "fc-green"),
    ("🗺️", "风险预警", "基于 XGBoost 模型与实时气象条件，预测区域病虫害风险等级", "XGBoost + 气象API", "fc-amber"),
    ("🤖", "AI 助手", "自然语言交互式查询，自动生成 SQL 并解读数据分析结果", "LLM + NL2SQL", "fc-blue"),
    ("📝", "分析报告", "一键生成专业级研究报告，涵盖数据分析与防治建议", "多Agent协作", "fc-purple"),
]
feature_card_row(modules)

st.markdown("")

# ── 技术架构 ──
st.markdown(
    '<div class="tech-flow">'
    '<div class="flow-title">🏗️ 技术架构</div>'
    '<div style="display:flex;align-items:center;justify-content:center;gap:0.6rem;flex-wrap:wrap;'
    'font-size:0.85rem;color:#6b7280;">'
    '<span style="background:linear-gradient(135deg,#d1fae5,#a7f3d0);color:#065f46;padding:0.4rem 1rem;border-radius:10px;font-weight:600;box-shadow:0 2px 6px rgba(5,150,105,0.12);">气象数据</span>'
    '<span style="color:#059669;font-weight:bold;">→</span>'
    '<span style="background:linear-gradient(135deg,#dbeafe,#bfdbfe);color:#1e40af;padding:0.4rem 1rem;border-radius:10px;font-weight:600;box-shadow:0 2px 6px rgba(37,99,235,0.1);">特征工程</span>'
    '<span style="color:#059669;font-weight:bold;">→</span>'
    '<span style="background:linear-gradient(135deg,#fef3c7,#fde68a);color:#92400e;padding:0.4rem 1rem;border-radius:10px;font-weight:600;box-shadow:0 2px 6px rgba(245,158,11,0.12);">XGBoost 预测</span>'
    '<span style="color:#059669;font-weight:bold;">→</span>'
    '<span style="background:linear-gradient(135deg,#ede9fe,#ddd6fe);color:#5b21b6;padding:0.4rem 1rem;border-radius:10px;font-weight:600;box-shadow:0 2px 6px rgba(124,58,237,0.1);">AI 分析</span>'
    '<span style="color:#059669;font-weight:bold;">→</span>'
    '<span style="background:linear-gradient(135deg,#fce7f3,#fbcfe8);color:#9d174d;padding:0.4rem 1rem;border-radius:10px;font-weight:600;box-shadow:0 2px 6px rgba(236,72,153,0.1);">可视化展示</span>'
    '</div></div>',
    unsafe_allow_html=True,
)

# ── 侧边栏 ──
with st.sidebar:
    st.markdown(
        '<div style="text-align:center;padding:1.5rem 0;">'
        '<div style="font-size:2.5rem;">🌾</div>'
        '<div style="font-size:1.1rem;font-weight:700;color:#ecfdf5;margin-top:0.5rem;">智慧农业预警系统</div>'
        '<div style="font-size:0.78rem;color:#6ee7b7;margin-top:0.3rem;letter-spacing:1px;">Smart Agri Pest Warning</div>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")

    # 用户信息卡片 — 参考 my-smart-farm 侧边栏用户卡片
    st.markdown(
        '<div style="background:rgba(5,150,105,0.15);border:1px solid rgba(110,231,183,0.2);'
        'border-radius:14px;padding:0.8rem 1rem;display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;">'
        '<div style="width:40px;height:40px;border-radius:50%;background:linear-gradient(135deg,#059669,#34d399);'
        'display:flex;align-items:center;justify-content:center;color:white;font-weight:bold;font-size:0.95rem;'
        'box-shadow:0 2px 8px rgba(5,150,105,0.3);">管</div>'
        '<div><div style="font-size:0.9rem;font-weight:700;color:#ecfdf5 !important;">系统管理员</div>'
        '<div style="font-size:0.72rem;color:#6ee7b7 !important;">区域植保监控</div></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    if db_path.exists():
        import os
        size_mb = os.path.getsize(db_path) / 1024 / 1024
        st.success(f"✅ 数据库就绪 · {size_mb:.1f} MB")
    else:
        st.warning("⚠️ 数据库未初始化")
        if st.button("一键初始化", use_container_width=True):
            from models.data_loader import init_database
            init_database()
            st.rerun()

    st.markdown("---")
    st.markdown(
        '<div style="text-align:center;font-size:0.72rem;color:#6ee7b7;opacity:0.6;">'
        'v2.0 · Powered by XGBoost & DeepSeek</div>',
        unsafe_allow_html=True,
    )
