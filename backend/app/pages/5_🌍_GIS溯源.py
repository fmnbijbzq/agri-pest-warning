"""🌍 GIS 时空溯源页面 — 参考 my-smart-farm GISView 组件"""
import streamlit as st
import sys
import json
import folium
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from streamlit_folium import st_folium

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header, section, stat_card
from utils.database import execute_query

st.set_page_config(page_title="GIS 时空溯源", page_icon="🌍", layout="wide")

inject_css()
page_header(
    "🌍 历史病虫害时空溯源系统",
    "基于 GIS 地图可视化病虫害时空扩散规律，支持按月回溯疫情演化过程",
    badge="GIS 可视化 · 时空分析 · 热力图",
)

# ── 省份中心坐标 ──
PROVINCE_COORDS = {
    "湖南": [27.61, 111.65], "湖北": [30.97, 112.27], "江西": [27.08, 114.94],
    "安徽": [31.74, 117.17], "江苏": [33.00, 119.79], "浙江": [29.15, 120.15],
    "四川": [30.26, 102.69], "河南": [33.88, 113.49], "河北": [38.04, 114.52],
    "山东": [36.37, 118.15], "广东": [23.13, 113.27], "广西": [23.73, 108.22],
    "云南": [24.97, 101.49], "黑龙江": [47.01, 127.10], "吉林": [43.54, 126.36],
    "辽宁": [41.67, 122.72], "福建": [25.93, 118.31],
}

# ── 风险等级颜色 ──
def risk_color(score):
    if score >= 0.7:
        return "#dc2626"
    elif score >= 0.5:
        return "#f97316"
    elif score >= 0.3:
        return "#eab308"
    else:
        return "#22c55e"


@st.cache_data(ttl=300)
def load_data():
    return execute_query("SELECT * FROM pest_history")


try:
    df = load_data()
except Exception:
    st.error("请先初始化数据库：回到首页点击初始化按钮")
    st.stop()

# ── 顶部过滤器 — 参考 my-smart-farm GIS 过滤栏 ──
section("筛选条件", "🔍")

f1, f2, f3, f4 = st.columns([2, 2, 2, 1])
with f1:
    years = sorted(df["year"].unique())
    year_sel = st.selectbox("📅 年份", years, index=len(years) - 1)
with f2:
    pests = ["全部"] + sorted(df["pest_name"].unique().tolist())
    pest_sel = st.selectbox("🐛 病虫害类型", pests)
with f3:
    crops = ["全部"] + sorted(df["crop"].unique().tolist())
    crop_sel = st.selectbox("🌱 作物", crops)
with f4:
    map_mode = st.selectbox("🗺️ 显示模式", ["热力图", "散点图"])

# 过滤数据
filtered = df[df["year"] == year_sel]
if pest_sel != "全部":
    filtered = filtered[filtered["pest_name"] == pest_sel]
if crop_sel != "全部":
    filtered = filtered[filtered["crop"] == crop_sel]

# ── 时间轴控制 — 参考 my-smart-farm 底部时间轴 ──
section("时间轴控制", "⏱️")

month_sel = st.slider(
    "选择月份查看疫情分布",
    min_value=1, max_value=12, value=7,
    format="%d月",
)

month_data = filtered[filtered["month"] == month_sel]

# 月份累计数据（到当前月）
cumulative = filtered[filtered["month"] <= month_sel]

# ── 当月统计 ──
st.markdown("")
c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    stat_card("📋", f"{len(month_data):,}", "当月记录", f"{month_sel}月")
with c2:
    stat_card("📊", f"{len(cumulative):,}", "累计记录", f"1-{month_sel}月")
with c3:
    avg_risk = month_data["risk_score"].mean() if len(month_data) > 0 else 0
    stat_card("⚡", f"{avg_risk:.1%}", "平均风险", "当月")
with c4:
    stat_card("🗺️", str(month_data["province"].nunique()), "涉及省份", "")
with c5:
    stat_card("🐛", str(month_data["pest_name"].nunique()), "病虫害种类", "")

st.markdown("")

# ── GIS 主体 — 左地图 + 右面板 ──
map_col, panel_col = st.columns([3, 1])

with map_col:
    section("疫情分布地图", "🗺️")

    # 按省份聚合
    if len(month_data) > 0:
        prov_stats = month_data.groupby("province").agg(
            count=("risk_score", "size"),
            avg_risk=("risk_score", "mean"),
            max_risk=("risk_score", "max"),
            top_pest=("pest_name", lambda x: x.mode().iloc[0] if len(x) > 0 else "无"),
        ).reset_index()
    else:
        import pandas as pd
        prov_stats = pd.DataFrame(columns=["province", "count", "avg_risk", "max_risk", "top_pest"])

    # 创建地图
    m = folium.Map(
        location=[32.0, 112.0],
        zoom_start=5,
        tiles=None,
    )
    # 高德中文底图
    folium.TileLayer(
        tiles="https://webrd02.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=8&x={x}&y={y}&z={z}",
        attr="高德地图",
        name="高德地图",
    ).add_to(m)

    if map_mode == "热力图" and len(month_data) > 0:
        # 热力图模式
        from folium.plugins import HeatMap
        heat_data = []
        for _, row in prov_stats.iterrows():
            if row["province"] in PROVINCE_COORDS:
                coords = PROVINCE_COORDS[row["province"]]
                # 权重 = 记录数 × 平均风险
                weight = row["count"] * row["avg_risk"]
                heat_data.append([coords[0], coords[1], weight])

        if heat_data:
            HeatMap(
                heat_data,
                radius=35,
                blur=25,
                max_zoom=8,
                gradient={0.2: "#22c55e", 0.4: "#eab308", 0.6: "#f97316", 0.8: "#ef4444", 1.0: "#7f1d1d"},
            ).add_to(m)

    # 散点图模式 或 热力图上叠加标记
    for _, row in prov_stats.iterrows():
        if row["province"] not in PROVINCE_COORDS:
            continue
        coords = PROVINCE_COORDS[row["province"]]
        color = risk_color(row["avg_risk"])
        radius = max(8, min(30, row["count"] / 2))

        popup_html = (
            f'<div style="font-family:sans-serif;min-width:180px;">'
            f'<b style="font-size:14px;color:#1f2937;">{row["province"]}</b><br>'
            f'<hr style="margin:4px 0;border-color:#e5e7eb;">'
            f'📋 记录数: <b>{int(row["count"])}</b><br>'
            f'⚡ 平均风险: <b style="color:{color};">{row["avg_risk"]:.1%}</b><br>'
            f'🔺 最高风险: <b>{row["max_risk"]:.1%}</b><br>'
            f'🐛 主要病虫害: <b>{row["top_pest"]}</b>'
            f'</div>'
        )

        if map_mode == "散点图":
            folium.CircleMarker(
                location=coords,
                radius=radius,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.6,
                weight=2,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f'{row["province"]} - 风险 {row["avg_risk"]:.0%}',
            ).add_to(m)
        else:
            # 热力图模式下加小标记
            folium.CircleMarker(
                location=coords,
                radius=5,
                color="#1f2937",
                fill=True,
                fill_color="#ffffff",
                fill_opacity=0.9,
                weight=1,
                popup=folium.Popup(popup_html, max_width=250),
                tooltip=f'{row["province"]}',
            ).add_to(m)

    st_folium(m, width=None, height=500, returned_objects=[])

with panel_col:
    # ── 右侧分析面板 — 参考 my-smart-farm 右侧面板 ──
    section("空间演化分析", "📊")

    if len(month_data) > 0:
        high_risk_provinces = prov_stats[prov_stats["avg_risk"] >= 0.5]
        n_high = len(high_risk_provinces)
        dominant_pest = month_data["pest_name"].mode().iloc[0] if len(month_data) > 0 else "无"

        st.markdown(
            f'<div class="white-card" style="font-size:0.85rem;line-height:1.8;color:#374151;">'
            f'基于 <b>{year_sel}年{month_sel}月</b> 数据，'
            f'<b style="color:#059669;">{dominant_pest}</b> 为当月主要病虫害，'
            f'共涉及 <b>{month_data["province"].nunique()}</b> 个省份。'
            f'{"<br>⚠️ 其中 <b style=color:#dc2626;>" + str(n_high) + " 个省份</b>处于中高风险区间。" if n_high > 0 else "<br>✅ 整体风险可控。"}'
            f'</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info("当前筛选条件下暂无数据")

    st.markdown("")

    # ── 区域高发排名 — 参考 my-smart-farm Top 3 ──
    section("区域高发排名", "🏆")

    if len(prov_stats) > 0:
        top_provinces = prov_stats.sort_values("count", ascending=False).head(5)
        max_count = top_provinces["count"].max()

        for i, (_, row) in enumerate(top_provinces.iterrows()):
            pct = row["count"] / max_count * 100
            color = risk_color(row["avg_risk"])
            st.markdown(
                f'<div style="margin-bottom:0.6rem;">'
                f'<div style="display:flex;justify-content:space-between;font-size:0.82rem;margin-bottom:2px;">'
                f'<span style="color:#4b5563;"><b>{i+1}.</b> {row["province"]}</span>'
                f'<span style="font-weight:700;color:{color};">{int(row["count"])}条 · {row["avg_risk"]:.0%}</span>'
                f'</div>'
                f'<div style="height:6px;background:#f3f4f6;border-radius:3px;overflow:hidden;">'
                f'<div style="height:100%;width:{pct}%;background:{color};border-radius:3px;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("暂无排名数据")

    st.markdown("")

    # ── 严重程度分布 ──
    section("严重程度", "📉")

    if len(month_data) > 0:
        sev_data = month_data["severity"].value_counts()
        colors = {"轻": "#34d399", "中": "#fbbf24", "重": "#f87171"}
        for sev in ["重", "中", "轻"]:
            val = sev_data.get(sev, 0)
            total = len(month_data)
            pct = val / total * 100 if total > 0 else 0
            c = colors.get(sev, "#9ca3af")
            st.markdown(
                f'<div style="margin-bottom:0.5rem;">'
                f'<div style="display:flex;justify-content:space-between;font-size:0.8rem;">'
                f'<span style="color:#6b7280;">{sev}</span>'
                f'<span style="font-weight:600;color:{c};">{val} ({pct:.0f}%)</span>'
                f'</div>'
                f'<div style="height:5px;background:#f3f4f6;border-radius:3px;overflow:hidden;">'
                f'<div style="height:100%;width:{pct}%;background:{c};border-radius:3px;"></div>'
                f'</div></div>',
                unsafe_allow_html=True,
            )

# ── 下方图表区域 ──
st.markdown("")
section("月度演化趋势", "📈")

chart1, chart2 = st.columns(2)

CHART_TEMPLATE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Noto Sans SC, sans-serif", size=12, color="#4b5563"),
    margin=dict(t=30, b=40, l=50, r=20),
)

with chart1:
    # 月度记录数趋势
    monthly = filtered.groupby("month").agg(
        count=("risk_score", "size"),
        avg_risk=("risk_score", "mean"),
    ).reset_index()

    fig1 = go.Figure()
    fig1.add_trace(go.Bar(
        x=monthly["month"], y=monthly["count"],
        name="记录数", marker_color="#a7f3d0", marker_cornerradius=4,
    ))
    fig1.add_trace(go.Scatter(
        x=monthly["month"], y=monthly["avg_risk"] * monthly["count"].max(),
        name="风险趋势", line=dict(color="#dc2626", width=2.5),
        yaxis="y2", mode="lines+markers", marker=dict(size=6),
    ))
    fig1.update_layout(
        **CHART_TEMPLATE, height=320,
        xaxis=dict(title="月份", dtick=1),
        yaxis=dict(title="记录数"),
        yaxis2=dict(overlaying="y", side="right", showgrid=False, showticklabels=False),
        legend=dict(orientation="h", y=1.12, x=0),
        bargap=0.3,
    )
    # 标记当前选中月份
    fig1.add_vline(x=month_sel, line_dash="dash", line_color="#059669", line_width=2,
                   annotation_text=f"当前: {month_sel}月", annotation_position="top")
    st.plotly_chart(fig1, use_container_width=True)

with chart2:
    # 各省份风险热力矩阵
    if len(filtered) > 0:
        pivot = filtered.groupby(["province", "month"])["risk_score"].mean().reset_index()
        pivot_table = pivot.pivot(index="province", columns="month", values="risk_score").fillna(0)

        fig2 = px.imshow(
            pivot_table,
            color_continuous_scale="RdYlGn_r",
            aspect="auto",
            labels=dict(x="月份", y="省份", color="风险"),
        )
        fig2.update_layout(**CHART_TEMPLATE, height=320, coloraxis_colorbar=dict(thickness=10, len=0.6))
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("暂无数据")
