"""共享 UI 设计系统 — 智慧农业病虫害预警系统 (现代化版本，参考 my-smart-farm 设计)"""
import streamlit as st

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 全局 CSS — 对标 my-smart-farm React UI 风格
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap');

/* ── 全局基础 ── */
html, body, [class*="css"] {
    font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
}
.main .block-container {
    padding: 1.5rem 2.5rem 3rem;
    max-width: 1400px;
}
section.main > div { padding-top: 0.5rem; }

/* ── 隐藏默认 Streamlit 元素 ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

/* ── 全局背景 ── */
.stApp {
    background: #F4F7F6;
}

/* ── 侧边栏 — 参考 my-smart-farm PC端深绿侧边栏 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1B3B36 0%, #064e3b 50%, #065f46 100%);
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 1rem;
}
section[data-testid="stSidebar"] * {
    color: #d1fae5 !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: #a7f3d0 !important;
    font-weight: 500;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(167,243,208,0.15);
}
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    color: #ecfdf5 !important;
    border-radius: 10px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    backdrop-filter: blur(10px);
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(52,211,153,0.2);
    border-color: rgba(110,231,183,0.4);
    transform: translateY(-1px);
}

/* ── 页面头部 — 参考 my-smart-farm 顶部 emerald 渐变条 ── */
.hero-header {
    background: linear-gradient(135deg, #1B3B36 0%, #064e3b 40%, #047857 100%);
    border-radius: 20px;
    padding: 2.2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(6,78,59,0.2);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60%; right: -15%;
    width: 500px; height: 500px;
    background: radial-gradient(circle, rgba(52,211,153,0.2) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -40%; left: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(167,243,208,0.12) 0%, transparent 70%);
    border-radius: 50%;
}
.hero-header h1 {
    color: #ffffff;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0;
    position: relative;
    z-index: 1;
    letter-spacing: 0.02em;
}
.hero-header .desc {
    color: #a7f3d0;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    position: relative;
    z-index: 1;
    font-weight: 300;
    line-height: 1.6;
}
.hero-header .badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.75rem;
    color: #d1fae5;
    margin-top: 0.8rem;
    position: relative;
    z-index: 1;
    font-weight: 500;
    letter-spacing: 0.5px;
}

/* ── 区块标题 — 参考 my-smart-farm 卡片标题风格 ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2.5rem 0 1.2rem;
    padding-bottom: 0.6rem;
    border-bottom: 2px solid #d1fae5;
}
.section-head .icon {
    width: 34px; height: 34px;
    background: linear-gradient(135deg, #059669, #10b981);
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    box-shadow: 0 2px 8px rgba(5,150,105,0.25);
}
.section-head .text {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1B3B36;
}

/* ── 指标卡片 — 参考 my-smart-farm KPI 卡片 ── */
.stat-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.4rem 1.2rem;
    text-align: center;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #059669, #34d399);
    border-radius: 3px 3px 0 0;
}
/* 参考 my-smart-farm 的右上角圆形装饰 */
.stat-card::after {
    content: '';
    position: absolute;
    top: -16px; right: -16px;
    width: 64px; height: 64px;
    background: linear-gradient(135deg, rgba(5,150,105,0.06), rgba(52,211,153,0.08));
    border-radius: 50%;
    transition: transform 0.35s ease;
}
.stat-card:hover::after {
    transform: scale(1.3);
}
.stat-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(5,150,105,0.15);
    border-color: #6ee7b7;
}
.stat-card .stat-icon { font-size: 1.6rem; margin-bottom: 0.4rem; }
.stat-card .stat-value {
    font-size: 1.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #059669, #047857);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    line-height: 1.3;
}
.stat-card .stat-label {
    font-size: 0.82rem;
    color: #6b7280;
    margin-top: 0.2rem;
    font-weight: 400;
}
.stat-card .stat-sub {
    font-size: 0.72rem;
    color: #9ca3af;
    margin-top: 0.1rem;
}

/* ── 风险仪表板 — 参考 my-smart-farm 风险状态卡片 ── */
.risk-banner {
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}
.risk-banner::after {
    content: '';
    position: absolute;
    top: 0; right: 0;
    width: 150px; height: 100%;
    opacity: 0.08;
    background-size: contain;
    background-repeat: no-repeat;
    background-position: center;
}
.risk-banner .risk-score {
    font-size: 3rem;
    font-weight: 900;
    line-height: 1;
}
.risk-banner .risk-label {
    font-size: 1.15rem;
    font-weight: 700;
    margin-left: 0.8rem;
}
.risk-banner .risk-meta {
    font-size: 0.85rem;
    opacity: 0.75;
    margin-top: 0.4rem;
}

.risk-low    { background: linear-gradient(135deg,#ecfdf5,#d1fae5); color:#065f46; border: 1px solid #a7f3d0; }
.risk-mid    { background: linear-gradient(135deg,#fffbeb,#fef3c7); color:#92400e; border: 1px solid #fcd34d; }
.risk-high   { background: linear-gradient(135deg,#fef2f2,#fecaca); color:#991b1b; border: 1px solid #f87171; }
.risk-extreme{ background: linear-gradient(135deg,#fee2e2,#fca5a5); color:#7f1d1d; border: 1px solid #ef4444; }

/* ── 功能卡片 — 参考 my-smart-farm feature card 风格 ── */
.feature-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 20px;
    padding: 2rem 1.4rem;
    text-align: center;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    min-height: 240px;
    position: relative;
    overflow: hidden;
}
.feature-card:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 40px rgba(5,150,105,0.15);
    border-color: #6ee7b7;
}
.feature-card .fc-icon {
    width: 60px; height: 60px;
    margin: 0 auto 1rem;
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.8rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.06);
}
.feature-card .fc-title {
    font-size: 1.1rem;
    font-weight: 700;
    color: #1B3B36;
    margin-bottom: 0.5rem;
}
.feature-card .fc-desc {
    font-size: 0.84rem;
    color: #6b7280;
    line-height: 1.6;
    margin-bottom: 1rem;
}
.feature-card .fc-tag {
    display: inline-block;
    padding: 0.25rem 0.8rem;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.3px;
}
.fc-green  .fc-icon { background: linear-gradient(135deg,#d1fae5,#a7f3d0); }
.fc-green  .fc-tag  { background:#d1fae5; color:#065f46; }
.fc-blue   .fc-icon { background: linear-gradient(135deg,#dbeafe,#bfdbfe); }
.fc-blue   .fc-tag  { background:#dbeafe; color:#1e40af; }
.fc-purple .fc-icon { background: linear-gradient(135deg,#ede9fe,#ddd6fe); }
.fc-purple .fc-tag  { background:#ede9fe; color:#5b21b6; }
.fc-amber  .fc-icon { background: linear-gradient(135deg,#fef3c7,#fde68a); }
.fc-amber  .fc-tag  { background:#fef3c7; color:#92400e; }

/* ── 引擎/状态标签 ── */
.engine-badge {
    background: rgba(16,185,129,0.15);
    border: 1px solid rgba(16,185,129,0.3);
    border-radius: 12px;
    padding: 0.7rem 1rem;
    text-align: center;
    font-weight: 600;
    font-size: 0.85rem;
    color: #d1fae5 !important;
    backdrop-filter: blur(10px);
}

/* ── 报告容器 ── */
.report-box {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 2.5rem 3rem;
    line-height: 2;
    font-size: 0.95rem;
    color: #374151;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
.report-box h1, .report-box h2, .report-box h3 {
    color: #065f46;
    border-bottom: 1px solid #d1fae5;
    padding-bottom: 0.4rem;
}

/* ── Plotly 图表容器 ── */
.stPlotlyChart {
    background: #ffffff;
    border: 1px solid #f3f4f6;
    border-radius: 14px;
    padding: 0.6rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
}

/* ── 主按钮 — 参考 my-smart-farm 绿色圆角按钮 ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #059669, #047857);
    border: none;
    border-radius: 12px;
    padding: 0.7rem 2rem;
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 14px rgba(5,150,105,0.35);
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 8px 25px rgba(5,150,105,0.45);
    transform: translateY(-2px);
}

/* ── 进度条 ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #059669, #34d399);
    border-radius: 10px;
}

/* ── 输入控件 ── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input {
    border-radius: 12px !important;
    border-color: #d1d5db !important;
    transition: all 0.3s ease;
}
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color: #34d399 !important;
    box-shadow: 0 0 0 2px rgba(52,211,153,0.2) !important;
}

/* ── 标签页 ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.8rem; }
.stTabs [data-baseweb="tab"] {
    border-radius: 10px 10px 0 0;
    font-weight: 500;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: #ecfdf5;
    border-bottom: 2px solid #059669;
}

/* ── 聊天消息 — 参考 my-smart-farm AI对话气泡 ── */
.stChatMessage {
    border-radius: 16px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04) !important;
    border: 1px solid #f3f4f6 !important;
}
[data-testid="stChatMessageContent"] {
    font-size: 0.95rem;
    line-height: 1.7;
}

/* ── 通用白色卡片容器 ── */
.white-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.5rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
    transition: all 0.3s ease;
}
.white-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
}

/* ── 预警响应等级条 — 参考 my-smart-farm 顶部红色badge ── */
.alert-bar {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.4rem 1rem;
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border: 1px solid #fca5a5;
    border-radius: 20px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #991b1b;
}

/* ── 技术架构流程条 ── */
.tech-flow {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.8rem 2rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.tech-flow .flow-title {
    font-weight: 700;
    color: #1B3B36;
    margin-bottom: 1rem;
    font-size: 0.95rem;
}

/* ── 侧边栏导航项美化 ── */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding: 0.5rem 0.8rem;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
    margin: 0.15rem 0;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    border-radius: 10px !important;
    padding: 0.5rem 0.8rem !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    font-weight: 500 !important;
    font-size: 0.92rem !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: rgba(52,211,153,0.15) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(52,211,153,0.2) !important;
    border-left: 3px solid #34d399 !important;
    font-weight: 700 !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
    font-size: 0.92rem !important;
}

/* ── 动画 ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(15px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-fadeIn {
    animation: fadeInUp 0.5s ease-out;
}

/* ── Slider 样式 ── */
.stSlider > div > div > div > div {
    background-color: #059669 !important;
}
</style>
"""


def inject_css():
    """注入全局样式"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, desc: str, badge: str = ""):
    """渲染页面头部横幅 — 参考 my-smart-farm 顶部导航"""
    badge_html = f'<div class="badge">{badge}</div>' if badge else ""
    st.markdown(
        f'<div class="hero-header">'
        f'<h1>{title}</h1>'
        f'<div class="desc">{desc}</div>'
        f'{badge_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def section(title: str, icon: str = ""):
    """带图标的区块标题"""
    icon_html = f'<div class="icon">{icon}</div>' if icon else ""
    st.markdown(
        f'<div class="section-head">{icon_html}'
        f'<div class="text">{title}</div></div>',
        unsafe_allow_html=True,
    )


def stat_card(icon: str, value: str, label: str, sub: str = ""):
    """数据指标卡片 — 参考 my-smart-farm KPI卡片"""
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
    st.markdown(
        f'<div class="stat-card">'
        f'<div class="stat-icon">{icon}</div>'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def feature_card(icon: str, title: str, desc: str, tag: str, color_class: str):
    """首页功能模块卡片"""
    st.markdown(
        f'<div class="feature-card {color_class}">'
        f'<div class="fc-icon">{icon}</div>'
        f'<div class="fc-title">{title}</div>'
        f'<div class="fc-desc">{desc}</div>'
        f'<span class="fc-tag">{tag}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def risk_banner(score: float, level: str, meta: str):
    """风险等级横幅"""
    if score >= 0.8:
        cls = "risk-extreme"
    elif score >= 0.6:
        cls = "risk-high"
    elif score >= 0.3:
        cls = "risk-mid"
    else:
        cls = "risk-low"
    st.markdown(
        f'<div class="risk-banner {cls}">'
        f'<span class="risk-score">{score:.0%}</span>'
        f'<span class="risk-label">{level}</span>'
        f'<div class="risk-meta">{meta}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
