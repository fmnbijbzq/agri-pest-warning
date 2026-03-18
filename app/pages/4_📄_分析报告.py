"""分析报告页面 (v3.0 专业级 UI)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header, section, stat_card_row, svg_icon
from config.settings import CROP_TYPES, PROVINCES

inject_css()
page_header(
    "研究报告生成",
    "基于数据分析结果，AI 自动生成符合学术规范的病虫害研究报告",
    badge="多Agent协作 · 一键生成 · 专业报告",
    icon="file-text",
)

# ── 参数设置 ──
section("报告参数", "settings")

col1, col2 = st.columns(2)
with col1:
    report_province = st.multiselect("分析省份", PROVINCES, default=["湖南", "湖北"])
    report_crop = st.selectbox("分析作物", CROP_TYPES)
with col2:
    report_title = st.text_input("报告标题", f"基于大数据的{report_crop}病虫害风险分析研究")
    year_range = st.slider("数据年份范围", 2018, 2025, (2020, 2025))

# 参数预览卡片
st.markdown(
    f'<div class="white-card" style="margin:1rem 0 1.5rem;">'
    f'<div style="display:flex;justify-content:space-around;align-items:center;text-align:center;'
    f'font-size:0.85rem;color:#4b5563;">'
    f'<span>{svg_icon("map-pin", 15, "#059669")} <b>{", ".join(report_province)}</b></span>'
    f'<span style="color:#e5e7eb;">|</span>'
    f'<span>{svg_icon("leaf", 15, "#059669")} <b>{report_crop}</b></span>'
    f'<span style="color:#e5e7eb;">|</span>'
    f'<span>{svg_icon("calendar", 15, "#059669")} <b>{year_range[0]}-{year_range[1]}</b></span>'
    f'</div></div>',
    unsafe_allow_html=True,
)

if st.button("生成研究报告", type="primary", use_container_width=True):
    progress_bar = st.progress(0, text="正在查询数据库...")

    try:
        from utils.database import execute_query
        from agents.datagen_integration import generate_research_report

        provinces_str = "','".join(report_province)
        df = execute_query(
            f"SELECT * FROM pest_history WHERE crop='{report_crop}' "
            f"AND province IN ('{provinces_str}') "
            f"AND year BETWEEN {year_range[0]} AND {year_range[1]}"
        )

        progress_bar.progress(20, text="正在统计分析数据...")

        analysis_data = {
            "title": report_title,
            "crop": report_crop,
            "provinces": report_province,
            "year_range": year_range,
            "total_records": len(df),
            "avg_risk": round(df["risk_score"].mean(), 3) if len(df) > 0 else 0,
            "top_pests": df["pest_name"].value_counts().head(5).to_dict() if len(df) > 0 else {},
            "severity_dist": df["severity"].value_counts().to_dict() if len(df) > 0 else {},
            "monthly_risk": df.groupby("month")["risk_score"].mean().to_dict() if len(df) > 0 else {},
            "weather_summary": {
                "avg_temp": round(df["temperature"].mean(), 1) if len(df) > 0 else 0,
                "avg_humidity": round(df["humidity"].mean(), 1) if len(df) > 0 else 0,
                "avg_rainfall": round(df["rainfall"].mean(), 1) if len(df) > 0 else 0,
            },
        }

        # 数据摘要
        section("数据摘要", "trending-up")

        ws = analysis_data["weather_summary"]
        stat_card_row([
            ("clipboard", f"{analysis_data['total_records']:,}", "数据量", "条"),
            ("zap", f"{analysis_data['avg_risk']:.1%}", "平均风险"),
            ("thermometer", f"{ws['avg_temp']}°C", "平均气温"),
            ("droplets", f"{ws['avg_humidity']}%", "平均湿度"),
            ("cloud-rain", f"{ws['avg_rainfall']}mm", "平均降雨"),
        ])

        st.markdown("")

        progress_bar.progress(40, text="AI 正在生成报告...")

        report_content = generate_research_report(analysis_data)

        progress_bar.progress(100, text="报告生成完成")

        section("报告正文", "file-text")

        st.markdown(
            f'<div class="report-box">{report_content}</div>',
            unsafe_allow_html=True,
        )

        st.markdown("")

        # 下载按钮
        section("导出报告", "download")

        dl1, dl2, dl3 = st.columns([2, 2, 1])
        with dl1:
            st.download_button(
                "下载 Markdown",
                data=report_content,
                file_name=f"{report_title}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with dl2:
            st.download_button(
                "下载纯文本",
                data=report_content,
                file_name=f"{report_title}.txt",
                mime="text/plain",
                use_container_width=True,
            )

    except Exception as e:
        progress_bar.empty()
        st.error(f"报告生成失败: {e}")
        st.info("请确保已配置 API Key 并初始化数据库")
