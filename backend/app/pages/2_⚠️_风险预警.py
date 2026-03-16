"""🗺 风险预警页面 (现代化版本)"""
import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from app.ui_style import inject_css, page_header, section, stat_card, stat_card_row, risk_banner
from config.settings import CROP_TYPES, PROVINCES

inject_css()
page_header(
    "🗺️ 风险预警",
    "输入当前气象条件，基于 XGBoost 模型实时预测病虫害风险等级",
    badge="XGBoost · 实时预测 · 智能决策",
)


@st.cache_resource
def load_model():
    import joblib
    from models.predictor import MODEL_DIR, train_risk_model
    model_path = MODEL_DIR / "risk_model.pkl"
    if not model_path.exists():
        train_risk_model()
    return joblib.load(model_path)


# ── 输入条件 ──
section("设置预测条件", "⚙️")

# 参考 my-smart-farm 的天气状态卡片布局
col1, col2, col3 = st.columns(3)
with col1:
    province = st.selectbox("🌍 选择省份", PROVINCES)
    crop = st.selectbox("🌱 选择作物", CROP_TYPES)
with col2:
    month = st.slider("📅 月份", 1, 12, 7)
    temperature = st.slider("🌡️ 平均气温 (°C)", -5.0, 45.0, 25.0, 0.5)
with col3:
    humidity = st.slider("💧 平均湿度 (%)", 20.0, 100.0, 70.0, 1.0)
    rainfall = st.slider("🌧️ 近期降雨 (mm)", 0.0, 100.0, 15.0, 1.0)

# 当前条件速览 — 参考 my-smart-farm 状态卡片中的天气行
st.markdown(
    f'<div class="white-card" style="margin:1rem 0 1.5rem;">'
    f'<div style="display:flex;justify-content:space-around;align-items:center;text-align:center;'
    f'font-size:0.9rem;color:#4b5563;">'
    f'<span>🌡️ <b>{temperature}°C</b></span>'
    f'<span style="color:#e5e7eb;">|</span>'
    f'<span>💧 <b>{humidity}%</b></span>'
    f'<span style="color:#e5e7eb;">|</span>'
    f'<span>🌧️ <b>{rainfall}mm</b></span>'
    f'<span style="color:#e5e7eb;">|</span>'
    f'<span>📅 <b>{month}月</b></span>'
    f'</div></div>',
    unsafe_allow_html=True,
)

if st.button("🔍 开始预测", type="primary", use_container_width=True):
    with st.spinner("模型推理中..."):
        from models.predictor import predict_risk
        result = predict_risk({
            "month": month, "province": province, "crop": crop,
            "temperature": temperature, "humidity": humidity, "rainfall": rainfall,
        })

    score = result["risk_score"]
    level = result["risk_level"]

    # ── 结果 ──
    section("预测结果", "🎯")

    risk_banner(score, level, f"{province} · {crop} · {month}月")

    st.progress(min(score, 1.0))

    stat_card_row([
        ("📊", f"{score:.1%}", "风险评分"),
        ("🏷️", level, "风险等级"),
        ("🌡️", f"{temperature}°C", "当前气温", f"湿度 {humidity}%"),
        ("🌧️", f"{rainfall}mm", "近期降雨"),
    ])

    st.markdown("")

    # ── 建议 — 参考 my-smart-farm 的预警建议风格 ──
    section("防治建议", "💡")

    if score >= 0.6:
        st.error(
            f"**⚠️ {level}** — 当前气象条件下 **{province}** 的 **{crop}** "
            f"病虫害风险较高，建议立即加强田间监测，必要时进行化学防治。\n\n"
            f"**建议措施：** 加大巡查频次 → 准备应急药剂 → 联系植保站获取专业指导"
        )
    elif score >= 0.3:
        st.warning(
            f"**🟡 {level}** — 存在一定风险，建议密切关注天气变化并做好预防性施药准备。\n\n"
            f"**建议措施：** 保持田间通风 → 适当调整灌溉 → 储备常用防治药剂"
        )
    else:
        st.success(
            f"**🟢 {level}** — 当前条件下病虫害风险较低，保持日常田间管理即可。\n\n"
            f"**建议措施：** 常规巡查 → 合理施肥 → 保持良好的田间生态环境"
        )
