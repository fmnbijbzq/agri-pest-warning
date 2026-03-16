"""智慧农业病虫害预警系统 — 主页 (v3.0 专业级 UI)"""
import streamlit as st
from pathlib import Path
import sys

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

st.set_page_config(
    page_title="首页 - 智慧农业预警",
    page_icon="🌾",
    layout="wide",
)

from app.ui_style import (
    inject_css, page_header, feature_card_row, stat_card_row,
    section, svg_icon, sidebar_brand, sidebar_user, sidebar_footer,
)

inject_css()

# ── Hero ──
page_header(
    "智慧农业病虫害预警系统",
    "基于大数据分析与 AI Agent 技术，为农业工作者提供病虫害智能预警和防治建议",
    badge="AI 驱动 · 数据赋能 · 精准防治",
    icon="sprout",
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

        section("核心数据指标", "trending-up")

        stat_card_row([
            ("clipboard", f"{int(row['cnt']):,}", "数据总量", "条历史记录"),
            ("map-pin", str(int(row['prov'])), "覆盖省份", "个监测区域"),
            ("leaf", str(int(row['crop'])), "作物种类", "种主要作物"),
            ("zap", f"{row['avg_risk']:.1%}", "平均风险", "全局风险均值"),
        ])
    except Exception:
        pass

st.markdown("")

# ── 功能模块 ──
section("功能模块", "layers")

modules = [
    ("bar-chart", "数据总览", "历史病虫害数据多维度可视化，支持省份、作物交叉筛选分析", "Plotly + Pandas", "fc-green"),
    ("alert-triangle", "风险预警", "基于 XGBoost 模型与实时气象条件，预测区域病虫害风险等级", "XGBoost + 气象API", "fc-amber"),
    ("bot", "AI 助手", "自然语言交互式查询，自动生成 SQL 并解读数据分析结果", "LLM + NL2SQL", "fc-blue"),
    ("file-text", "分析报告", "一键生成专业级研究报告，涵盖数据分析与防治建议", "多Agent协作", "fc-purple"),
]
feature_card_row(modules)

st.markdown("")

# ── 技术架构 ──
flow_steps = [
    ("#d1fae5", "#065f46", "cloud-rain", "气象数据"),
    ("#dbeafe", "#1e40af", "cpu", "特征工程"),
    ("#fef3c7", "#92400e", "activity", "XGBoost 预测"),
    ("#ede9fe", "#5b21b6", "sparkles", "AI 分析"),
    ("#fce7f3", "#9d174d", "pie-chart", "可视化展示"),
]

steps_html = ""
for i, (bg, fg, icon, label) in enumerate(flow_steps):
    steps_html += (
        f'<span class="flow-step" style="background:{bg};color:{fg};">'
        f'{svg_icon(icon, 15, fg)}{label}</span>'
    )
    if i < len(flow_steps) - 1:
        steps_html += f'<span class="flow-arrow">{svg_icon("chevron-right", 16, "#34d399")}</span>'

st.markdown(
    f'<div class="tech-flow">'
    f'<div class="flow-title">{svg_icon("box", 18, "#059669")}技术架构</div>'
    f'<div style="display:flex;align-items:center;justify-content:center;gap:0.4rem;flex-wrap:wrap;">'
    f'{steps_html}'
    f'</div></div>',
    unsafe_allow_html=True,
)

# ── 侧边栏 ──
with st.sidebar:
    sidebar_brand()
    sidebar_user()

    if db_path.exists():
        import os
        size_mb = os.path.getsize(db_path) / 1024 / 1024
        st.success(f"数据库就绪 · {size_mb:.1f} MB")
    else:
        st.warning("数据库未初始化")
        if st.button("一键初始化", use_container_width=True):
            from models.data_loader import init_database
            init_database()
            st.rerun()

    sidebar_footer()
