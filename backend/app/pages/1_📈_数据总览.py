"""📊 数据总览页面 (现代化版本)"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header, section, stat_card
from utils.database import execute_query

inject_css()
page_header(
    "📊 数据总览",
    "历史病虫害数据多维度可视化分析，支持作物和省份交叉筛选",
    badge="Plotly 可视化 · 实时筛选",
)

# Plotly 全局模板 — 更现代的视觉风格
CHART_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans SC, sans-serif", size=12, color="#4b5563"),
    margin=dict(t=30, b=40, l=50, r=20),
    hoverlabel=dict(bgcolor="#ffffff", font_size=13, bordercolor="#d1fae5",
                    font=dict(family="Noto Sans SC, sans-serif")),
)


@st.cache_data(ttl=300)
def load_pest_data():
    return execute_query("SELECT * FROM pest_history")


try:
    df = load_pest_data()
except Exception:
    st.error("请先初始化数据库：回到主页点击初始化按钮")
    st.stop()

# ── 筛选器 ──
section("数据筛选", "🔍")

col1, col2 = st.columns(2)
with col1:
    crop_filter = st.multiselect(
        "🌱 选择作物", list(df["crop"].unique()), default=list(df["crop"].unique())
    )
with col2:
    province_filter = st.multiselect(
        "🌍 选择省份", list(df["province"].unique()), default=list(df["province"].unique()[:5])
    )

filtered = df[(df["crop"].isin(crop_filter)) & (df["province"].isin(province_filter))]

# ── 概览 ──
section("数据概览", "📈")

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    stat_card("📋", f"{len(filtered):,}", "筛选记录", f"共 {len(df):,} 条")
with c2:
    stat_card("🗺️", str(filtered["province"].nunique()), "覆盖省份", "")
with c3:
    stat_card("🌱", str(filtered["crop"].nunique()), "作物种类", "")
with c4:
    avg_r = filtered["risk_score"].mean() if len(filtered) > 0 else 0
    stat_card("⚡", f"{avg_r:.1%}", "平均风险", "")
with c5:
    stat_card("🐛", str(filtered["pest_name"].nunique()) if len(filtered) > 0 else "0", "病虫害种类", "")

# ── 省份分析 ──
section("省份分析", "🗺️")

tab1, tab2 = st.tabs(["📊 记录分布", "🎯 风险对比"])

with tab1:
    prov_data = filtered.groupby("province").size().reset_index(name="count").sort_values("count", ascending=False)
    fig1 = px.bar(prov_data, x="province", y="count", color="count",
                  color_continuous_scale=["#a7f3d0", "#059669", "#064e3b"])
    fig1.update_layout(**CHART_TEMPLATE, height=380, showlegend=False, coloraxis_showscale=False,
                        xaxis_title="", yaxis_title="记录数")
    fig1.update_traces(marker_line_width=0, marker_cornerradius=8)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    if len(filtered) > 0:
        prov_risk = filtered.groupby("province")["risk_score"].mean().reset_index().sort_values("risk_score")
        fig1b = px.bar(prov_risk, x="risk_score", y="province", orientation="h",
                       color="risk_score", color_continuous_scale="RdYlGn_r")
        fig1b.update_layout(**CHART_TEMPLATE, height=380, showlegend=False, coloraxis_showscale=False,
                            xaxis_title="平均风险评分", yaxis_title="")
        fig1b.update_traces(marker_line_width=0, marker_cornerradius=8)
        st.plotly_chart(fig1b, use_container_width=True)

# ── 时间 & 严重程度 ──
section("时间与严重程度", "📅")

chart_a, chart_b = st.columns(2)

with chart_a:
    fig2 = px.histogram(
        filtered, x="month", color="severity", barmode="group",
        category_orders={"severity": ["轻", "中", "重"]},
        color_discrete_map={"轻": "#34d399", "中": "#fbbf24", "重": "#f87171"},
    )
    fig2.update_layout(**CHART_TEMPLATE, height=360, xaxis_title="月份", yaxis_title="记录数",
                        legend_title="严重程度", xaxis=dict(dtick=1))
    fig2.update_traces(marker_line_width=0, marker_cornerradius=6)
    st.plotly_chart(fig2, use_container_width=True)

with chart_b:
    top_pests = filtered["pest_name"].value_counts().head(8).reset_index()
    top_pests.columns = ["pest_name", "count"]
    fig4 = px.bar(top_pests, x="count", y="pest_name", orientation="h",
                  color="count", color_continuous_scale=["#fecaca", "#ef4444", "#991b1b"])
    fig4.update_layout(**CHART_TEMPLATE, height=360, showlegend=False, coloraxis_showscale=False,
                        xaxis_title="发生次数", yaxis_title="", yaxis=dict(autorange="reversed"))
    fig4.update_traces(marker_line_width=0, marker_cornerradius=6)
    st.plotly_chart(fig4, use_container_width=True)

# ── 气象关联 ──
section("气象 — 风险关联分析", "🌡️")

sample = filtered.sample(min(800, len(filtered))) if len(filtered) > 0 else filtered
fig3 = px.scatter(
    sample, x="temperature", y="humidity", color="risk_score",
    size="rainfall", hover_data=["crop", "pest_name", "province"],
    color_continuous_scale="RdYlGn_r", opacity=0.75,
)
fig3.update_layout(**CHART_TEMPLATE, height=460, xaxis_title="温度 (°C)", yaxis_title="湿度 (%)",
                    coloraxis_colorbar=dict(title="风险", thickness=14, len=0.6))
st.plotly_chart(fig3, use_container_width=True)
