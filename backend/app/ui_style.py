"""共享 UI 设计系统 — 智慧农业病虫害预警系统 (v3.0 专业级 UI)"""
import streamlit as st

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SVG 图标系统 — 替代 emoji，使用 Lucide 风格 24x24 SVG
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
_ICONS = {
    # 导航 & 通用
    "home": '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>',
    "search": '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06A1.65 1.65 0 0 0 4.68 15a1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06A1.65 1.65 0 0 0 9 4.68a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06A1.65 1.65 0 0 0 19.4 9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "filter": '<polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/>',
    "clock": '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/>',
    "box": '<path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>',

    # 数据 & 图表
    "bar-chart": '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>',
    "trending-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline points="17 6 23 6 23 12"/>',
    "pie-chart": '<path d="M21.21 15.89A10 10 0 1 1 8 2.83"/><path d="M22 12A10 10 0 0 0 12 2v10z"/>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>',
    "database": '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/>',
    "clipboard": '<path d="M16 4h2a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V6a2 2 0 0 1 2-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/>',

    # 农业 & 自然
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.9C15.5 4.9 17 3.5 19 2c1 2 2 4.5 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "sprout": '<path d="M7 20h10"/><path d="M10 20c5.5-2.5.8-6.4 3-10"/><path d="M9.5 9.4c1.1.8 1.8 2.2 2.3 3.7-2 .4-3.5.4-4.8-.3-1.2-.6-2.3-1.9-3-4.2 2.8-.5 4.4 0 5.5.8z"/><path d="M14.1 6a7 7 0 0 0-1.1 4c1.9-.1 3.3-.6 4.3-1.4 1-1 1.6-2.3 1.7-4.6-2.7.1-4 1-4.9 2z"/>',
    "sun": '<circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>',
    "thermometer": '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>',
    "droplets": '<path d="M7 16.3c2.2 0 4-1.83 4-4.05 0-1.16-.57-2.26-1.71-3.19S7.29 6.75 7 5.3c-.29 1.45-1.14 2.84-2.29 3.76S3 11.1 3 12.25c0 2.22 1.8 4.05 4 4.05z"/><path d="M12.56 6.6A10.97 10.97 0 0 0 14 3.02c.5 2.5 2 4.9 4 6.5s3 3.5 3 5.5a6.98 6.98 0 0 1-11.91 4.97"/>',
    "cloud-rain": '<line x1="16" y1="13" x2="16" y2="21"/><line x1="8" y1="13" x2="8" y2="21"/><line x1="12" y1="15" x2="12" y2="23"/><path d="M20 16.58A5 5 0 0 0 18 7h-1.26A8 8 0 1 0 4 15.25"/>',
    "bug": '<rect x="8" y="6" width="8" height="14" rx="4"/><path d="m19 7-3 2"/><path d="m5 7 3 2"/><path d="m19 19-3-2"/><path d="m5 19 3-2"/><path d="M20 13h-4"/><path d="M4 13h4"/><line x1="12" y1="6" x2="12" y2="2"/>',

    # AI & 技术
    "bot": '<rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"/><rect x="9" y="9" width="6" height="6"/><line x1="9" y1="1" x2="9" y2="4"/><line x1="15" y1="1" x2="15" y2="4"/><line x1="9" y1="20" x2="9" y2="23"/><line x1="15" y1="20" x2="15" y2="23"/><line x1="20" y1="9" x2="23" y2="9"/><line x1="20" y1="14" x2="23" y2="14"/><line x1="1" y1="9" x2="4" y2="9"/><line x1="1" y1="14" x2="4" y2="14"/>',
    "sparkles": '<path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/><path d="M5 3v4"/><path d="M19 17v4"/><path d="M3 5h4"/><path d="M17 19h4"/>',
    "message-circle": '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>',
    "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/>',
    "rocket": '<path d="M4.5 16.5c-1.5 1.26-2 5-2 5s3.74-.5 5-2c.71-.84.7-2.13-.09-2.91a2.18 2.18 0 0 0-2.91-.09z"/><path d="m12 15-3-3a22 22 0 0 1 2-3.95A12.88 12.88 0 0 1 22 2c0 2.72-.78 7.5-6 11a22.35 22.35 0 0 1-4 2z"/><path d="M9 12H4s.55-3.03 2-4c1.62-1.08 5 0 5 0"/><path d="M12 15v5s3.03-.55 4-2c1.08-1.62 0-5 0-5"/>',

    # 地图 & 位置
    "globe": '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>',
    "map-pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/>',
    "map": '<polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"/><line x1="8" y1="2" x2="8" y2="18"/><line x1="16" y1="6" x2="16" y2="22"/>',
    "compass": '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>',

    # 状态 & 通知
    "alert-triangle": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="12"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    "lightbulb": '<path d="M15 14c.2-1 .7-1.7 1.5-2.5 1-.9 1.5-2.2 1.5-3.5A6 6 0 0 0 6 8c0 1 .2 2.2 1.5 3.5.7.7 1.3 1.5 1.5 2.5"/><path d="M9 18h6"/><path d="M10 22h4"/>',
    "award": '<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>',
    "trophy": '<path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/>',
    "calendar": '<rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "trash": '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/>',
    "chevron-right": '<polyline points="9 18 15 12 9 6"/>',
    "external-link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
}


def svg_icon(name: str, size: int = 24, color: str = "currentColor", cls: str = "") -> str:
    """生成内联 SVG 图标 HTML"""
    path = _ICONS.get(name, _ICONS["info"])
    class_attr = f' class="{cls}"' if cls else ""
    return (
        f'<svg{class_attr} xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" '
        f'stroke-linecap="round" stroke-linejoin="round">{path}</svg>'
    )


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 全局 CSS — 专业级设计系统
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Noto+Sans+SC:wght@300;400;500;600;700;900&display=swap');

/* ── 强制亮色模式 ── */
:root {
    color-scheme: light only;
    --emerald-50: #ecfdf5;
    --emerald-100: #d1fae5;
    --emerald-200: #a7f3d0;
    --emerald-300: #6ee7b7;
    --emerald-400: #34d399;
    --emerald-500: #10b981;
    --emerald-600: #059669;
    --emerald-700: #047857;
    --emerald-800: #065f46;
    --emerald-900: #064e3b;
    --emerald-950: #1B3B36;
    --gray-50: #f9fafb;
    --gray-100: #f3f4f6;
    --gray-200: #e5e7eb;
    --gray-300: #d1d5db;
    --gray-400: #9ca3af;
    --gray-500: #6b7280;
    --gray-600: #4b5563;
    --gray-700: #374151;
    --gray-800: #1f2937;
    --gray-900: #111827;
    --bg: #f0f5f3;
    --card-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.02);
    --card-shadow-hover: 0 10px 25px rgba(5,150,105,0.1), 0 4px 10px rgba(0,0,0,0.04);
    --radius: 14px;
    --radius-lg: 18px;
    --transition: 0.25s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── 全局基础 ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
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
.stApp { background: var(--bg); }
.main, section.main, [data-testid="stAppViewContainer"] {
    background: var(--bg);
    color: var(--emerald-950);
}
header[data-testid="stHeader"] { background: var(--bg); }

/* ── 侧边栏 ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #142e29 0%, var(--emerald-900) 50%, var(--emerald-800) 100%);
    box-shadow: 4px 0 24px rgba(0,0,0,0.12);
}
section[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.5rem;
}
section[data-testid="stSidebar"] * {
    color: var(--emerald-100) !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] .stMultiSelect label {
    color: var(--emerald-200) !important;
    font-weight: 500;
    font-size: 0.82rem;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
section[data-testid="stSidebar"] hr {
    border-color: rgba(167,243,208,0.1);
    margin: 0.8rem 0;
}
section[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.1);
    color: var(--emerald-50) !important;
    border-radius: 10px;
    transition: all var(--transition);
    backdrop-filter: blur(10px);
    font-weight: 500;
    font-size: 0.85rem;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(52,211,153,0.15);
    border-color: rgba(110,231,183,0.3);
}

/* ── 页面头部 Hero ── */
.hero-header {
    background: linear-gradient(135deg, #142e29 0%, var(--emerald-900) 35%, var(--emerald-700) 100%);
    border-radius: var(--radius-lg);
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 8px 30px rgba(6,78,59,0.18), inset 0 1px 0 rgba(255,255,255,0.05);
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -50%; right: -10%;
    width: 400px; height: 400px;
    background: radial-gradient(circle, rgba(52,211,153,0.15) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-header::after {
    content: '';
    position: absolute;
    bottom: -30%; left: -5%;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(167,243,208,0.08) 0%, transparent 70%);
    border-radius: 50%;
    pointer-events: none;
}
.hero-header h1 {
    color: #ffffff;
    font-size: 1.65rem;
    font-weight: 700;
    margin: 0;
    position: relative;
    z-index: 1;
    letter-spacing: -0.01em;
    display: flex;
    align-items: center;
    gap: 0.6rem;
}
.hero-header h1 svg {
    flex-shrink: 0;
    opacity: 0.9;
}
.hero-header .desc {
    color: var(--emerald-200);
    font-size: 0.9rem;
    margin-top: 0.5rem;
    position: relative;
    z-index: 1;
    font-weight: 400;
    line-height: 1.6;
    opacity: 0.85;
}
.hero-header .badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.72rem;
    color: var(--emerald-200);
    margin-top: 0.8rem;
    position: relative;
    z-index: 1;
    font-weight: 500;
    letter-spacing: 0.3px;
}

/* ── 区块标题 ── */
.section-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 1rem;
    padding-bottom: 0.6rem;
    border-bottom: 1px solid var(--emerald-100);
}
.section-head .icon-box {
    width: 32px; height: 32px;
    background: linear-gradient(135deg, var(--emerald-600), var(--emerald-500));
    border-radius: 9px;
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
    box-shadow: 0 2px 6px rgba(5,150,105,0.2);
}
.section-head .icon-box svg {
    width: 16px; height: 16px;
}
.section-head .text {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--emerald-950);
    letter-spacing: -0.01em;
}

/* ── 指标卡片 ── */
.stat-card {
    background: #ffffff;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.3rem 1rem;
    text-align: center;
    transition: all var(--transition);
    box-shadow: var(--card-shadow);
    position: relative;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    min-height: 140px;
    box-sizing: border-box;
    cursor: default;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--emerald-500), var(--emerald-400));
    opacity: 0;
    transition: opacity var(--transition);
}
.stat-card:hover::before {
    opacity: 1;
}
.stat-card:hover {
    box-shadow: var(--card-shadow-hover);
    border-color: var(--emerald-200);
}
.stat-card .stat-icon {
    width: 40px; height: 40px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    margin-bottom: 0.6rem;
    background: var(--emerald-50);
}
.stat-card .stat-icon svg {
    width: 20px; height: 20px;
    stroke: var(--emerald-600);
}
.stat-card .stat-value {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--emerald-950);
    line-height: 1.2;
    white-space: nowrap;
    letter-spacing: -0.02em;
}
.stat-card .stat-label {
    font-size: 0.78rem;
    color: var(--gray-500);
    margin-top: 0.15rem;
    font-weight: 500;
}
.stat-card .stat-sub {
    font-size: 0.68rem;
    color: var(--gray-400);
    margin-top: 0.1rem;
}

/* ── 风险仪表板 ── */
.risk-banner {
    border-radius: var(--radius-lg);
    padding: 1.6rem 2rem;
    margin: 1rem 0;
    position: relative;
    overflow: hidden;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 0.5rem;
}
.risk-banner .risk-score {
    font-size: 2.8rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.03em;
}
.risk-banner .risk-label {
    font-size: 1.1rem;
    font-weight: 700;
    margin-left: 0.6rem;
}
.risk-banner .risk-meta {
    width: 100%;
    font-size: 0.82rem;
    opacity: 0.7;
    margin-top: 0.2rem;
}
.risk-low     { background: linear-gradient(135deg,#ecfdf5,#d1fae5); color:#065f46; border: 1px solid #a7f3d0; }
.risk-mid     { background: linear-gradient(135deg,#fffbeb,#fef3c7); color:#92400e; border: 1px solid #fcd34d; }
.risk-high    { background: linear-gradient(135deg,#fef2f2,#fecaca); color:#991b1b; border: 1px solid #f87171; }
.risk-extreme { background: linear-gradient(135deg,#fee2e2,#fca5a5); color:#7f1d1d; border: 1px solid #ef4444; }

/* ── 功能卡片 ── */
.feature-card {
    background: #ffffff;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius-lg);
    padding: 1.8rem 1.4rem;
    text-align: center;
    transition: all var(--transition);
    box-shadow: var(--card-shadow);
    min-height: 230px;
    box-sizing: border-box;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    position: relative;
    overflow: hidden;
    cursor: pointer;
}
.feature-card:hover {
    box-shadow: var(--card-shadow-hover);
    border-color: var(--emerald-200);
}
.feature-card .fc-icon {
    width: 56px; height: 56px;
    margin: 0 auto 1rem;
    border-radius: 14px;
    display: flex; align-items: center; justify-content: center;
}
.feature-card .fc-icon svg {
    width: 26px; height: 26px;
}
.feature-card .fc-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: var(--emerald-950);
    margin-bottom: 0.4rem;
    letter-spacing: -0.01em;
}
.feature-card .fc-desc {
    font-size: 0.82rem;
    color: var(--gray-500);
    line-height: 1.6;
    margin-bottom: 0.8rem;
}
.feature-card .fc-tag {
    display: inline-block;
    padding: 0.2rem 0.75rem;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.2px;
}
.fc-green  .fc-icon { background: linear-gradient(135deg,#d1fae5,#a7f3d0); }
.fc-green  .fc-icon svg { stroke: #059669; }
.fc-green  .fc-tag  { background:#d1fae5; color:#065f46; }
.fc-blue   .fc-icon { background: linear-gradient(135deg,#dbeafe,#bfdbfe); }
.fc-blue   .fc-icon svg { stroke: #2563eb; }
.fc-blue   .fc-tag  { background:#dbeafe; color:#1e40af; }
.fc-purple .fc-icon { background: linear-gradient(135deg,#ede9fe,#ddd6fe); }
.fc-purple .fc-icon svg { stroke: #7c3aed; }
.fc-purple .fc-tag  { background:#ede9fe; color:#5b21b6; }
.fc-amber  .fc-icon { background: linear-gradient(135deg,#fef3c7,#fde68a); }
.fc-amber  .fc-icon svg { stroke: #d97706; }
.fc-amber  .fc-tag  { background:#fef3c7; color:#92400e; }

/* ── 引擎标签 ── */
.engine-badge {
    background: rgba(16,185,129,0.12);
    border: 1px solid rgba(16,185,129,0.2);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    text-align: center;
    font-weight: 600;
    font-size: 0.82rem;
    color: var(--emerald-100) !important;
}

/* ── 报告容器 ── */
.report-box {
    background: #ffffff;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 2.5rem 3rem;
    line-height: 2;
    font-size: 0.92rem;
    color: var(--gray-700);
    box-shadow: var(--card-shadow);
}
.report-box h1, .report-box h2, .report-box h3 {
    color: var(--emerald-800);
    border-bottom: 1px solid var(--emerald-100);
    padding-bottom: 0.4rem;
}

/* ── Plotly 图表容器 ── */
.stPlotlyChart {
    background: #ffffff;
    border: 1px solid var(--gray-100);
    border-radius: var(--radius);
    padding: 0.5rem;
    box-shadow: var(--card-shadow);
}

/* ── 主按钮 ── */
.stButton > button[kind="primary"],
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, var(--emerald-600), var(--emerald-700));
    border: none;
    border-radius: 11px;
    padding: 0.65rem 2rem;
    font-weight: 600;
    font-size: 0.9rem;
    letter-spacing: 0.3px;
    transition: all var(--transition);
    box-shadow: 0 2px 8px rgba(5,150,105,0.25);
}
.stButton > button[kind="primary"]:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    box-shadow: 0 4px 16px rgba(5,150,105,0.35);
}

/* ── 进度条 ── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--emerald-600), var(--emerald-400));
    border-radius: 10px;
}

/* ── 输入控件 ── */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stTextInput > div > div > input {
    border-radius: 11px !important;
    border-color: var(--gray-300) !important;
    background-color: #ffffff !important;
    color: var(--gray-700) !important;
    transition: all 0.2s ease;
    font-size: 0.88rem;
}
.stSelectbox > div > div:focus-within,
.stMultiSelect > div > div:focus-within,
.stTextInput > div > div > input:focus {
    border-color: var(--emerald-400) !important;
    box-shadow: 0 0 0 2px rgba(52,211,153,0.15) !important;
}
[data-baseweb="popover"], [data-baseweb="menu"], [data-baseweb="select"] ul {
    background-color: #ffffff !important;
    color: var(--gray-700) !important;
    border-radius: 11px !important;
    box-shadow: 0 8px 24px rgba(0,0,0,0.08) !important;
}
[data-baseweb="menu"] li { color: var(--gray-700) !important; }
[data-baseweb="menu"] li:hover { background-color: var(--emerald-50) !important; }
.main .stSelectbox label,
.main .stMultiSelect label,
.main .stTextInput label,
.main .stSlider label {
    color: var(--gray-700) !important;
    font-weight: 500;
    font-size: 0.85rem;
}

/* ── 标签页 ── */
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; }
.stTabs [data-baseweb="tab"] {
    border-radius: 9px 9px 0 0;
    font-weight: 500;
    font-size: 0.88rem;
    transition: all 0.2s;
    padding: 0.5rem 1rem;
}
.stTabs [aria-selected="true"] {
    background: var(--emerald-50);
    border-bottom: 2px solid var(--emerald-600);
    font-weight: 600;
}

/* ── 聊天消息 ── */
.stChatMessage {
    border-radius: var(--radius) !important;
    box-shadow: var(--card-shadow) !important;
    border: 1px solid var(--gray-100) !important;
}
[data-testid="stChatMessageContent"] {
    font-size: 0.92rem;
    line-height: 1.7;
}

/* ── 通用白色卡片容器 ── */
.white-card {
    background: #ffffff;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.2rem 1.5rem;
    box-shadow: var(--card-shadow);
    transition: all var(--transition);
}
.white-card:hover {
    box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}

/* ── 预警条 ── */
.alert-bar {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.35rem 0.9rem;
    background: linear-gradient(135deg, #fef2f2, #fee2e2);
    border: 1px solid #fca5a5;
    border-radius: 20px;
    font-size: 0.78rem;
    font-weight: 600;
    color: #991b1b;
}

/* ── 技术架构流程条 ── */
.tech-flow {
    background: #ffffff;
    border: 1px solid var(--gray-200);
    border-radius: var(--radius);
    padding: 1.5rem 2rem;
    box-shadow: var(--card-shadow);
}
.tech-flow .flow-title {
    font-weight: 700;
    color: var(--emerald-950);
    margin-bottom: 1rem;
    font-size: 0.92rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.tech-flow .flow-title svg {
    width: 18px; height: 18px;
    stroke: var(--emerald-600);
}
.flow-step {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.4rem 1rem;
    border-radius: 9px;
    font-weight: 600;
    font-size: 0.8rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    white-space: nowrap;
}
.flow-step svg {
    width: 15px; height: 15px;
    flex-shrink: 0;
}
.flow-arrow {
    color: var(--emerald-400);
    font-size: 0.9rem;
    font-weight: 700;
    margin: 0 0.1rem;
}

/* ── 侧边栏导航项 ── */
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
    padding: 0.3rem 0.6rem;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
    margin: 0.1rem 0;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
    border-radius: 9px !important;
    padding: 0.45rem 0.7rem !important;
    transition: all 0.2s ease !important;
    font-weight: 500 !important;
    font-size: 0.88rem !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
    background: rgba(52,211,153,0.1) !important;
}
section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: rgba(52,211,153,0.15) !important;
    border-left: 3px solid var(--emerald-400) !important;
    font-weight: 600 !important;
}

/* ── 动画 ── */
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(12px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
.animate-fadeIn {
    animation: fadeInUp 0.4s ease-out;
}

/* ── prefers-reduced-motion ── */
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        animation-iteration-count: 1 !important;
        transition-duration: 0.01ms !important;
    }
}

/* ── 卡片行 Grid 布局 ── */
.stat-card-row {
    display: grid;
    gap: 0.8rem;
    margin: 0.5rem 0;
}
.feature-card-row {
    display: grid;
    gap: 1rem;
    margin: 0.5rem 0;
}

/* ── 响应式 ── */
@media (max-width: 768px) {
    .stat-card-row, .feature-card-row {
        grid-template-columns: repeat(2, 1fr) !important;
    }
    .hero-header {
        padding: 1.5rem;
    }
    .hero-header h1 {
        font-size: 1.3rem;
    }
}
@media (max-width: 480px) {
    .stat-card-row, .feature-card-row {
        grid-template-columns: 1fr !important;
    }
}

/* ── Slider 样式 ── */
.stSlider > div > div > div > div {
    background-color: var(--emerald-600) !important;
}

/* ── 侧边栏品牌 ── */
.sidebar-brand {
    text-align: center;
    padding: 1.2rem 0 0.8rem;
}
.sidebar-brand .brand-icon {
    width: 48px; height: 48px;
    border-radius: 14px;
    background: linear-gradient(135deg, var(--emerald-500), var(--emerald-400));
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.5rem;
    box-shadow: 0 4px 12px rgba(5,150,105,0.3);
}
.sidebar-brand .brand-icon svg {
    width: 26px; height: 26px;
    stroke: #ffffff;
}
.sidebar-brand .brand-title {
    font-size: 1rem;
    font-weight: 700;
    color: var(--emerald-50) !important;
    margin-top: 0.3rem;
}
.sidebar-brand .brand-sub {
    font-size: 0.72rem;
    color: var(--emerald-300) !important;
    margin-top: 0.15rem;
    letter-spacing: 0.5px;
    font-weight: 400;
}

/* ── 侧边栏用户卡片 ── */
.sidebar-user {
    background: rgba(5,150,105,0.1);
    border: 1px solid rgba(110,231,183,0.12);
    border-radius: 12px;
    padding: 0.7rem 0.9rem;
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin-bottom: 0.8rem;
}
.sidebar-user .avatar {
    width: 36px; height: 36px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--emerald-600), var(--emerald-400));
    display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
}
.sidebar-user .avatar svg {
    width: 18px; height: 18px;
    stroke: #ffffff;
}
.sidebar-user .name {
    font-size: 0.85rem;
    font-weight: 600;
    color: var(--emerald-50) !important;
}
.sidebar-user .role {
    font-size: 0.7rem;
    color: var(--emerald-300) !important;
}

/* ── 侧边栏底部版本 ── */
.sidebar-version {
    text-align: center;
    font-size: 0.7rem;
    color: var(--emerald-300) !important;
    opacity: 0.5;
    padding: 0.5rem 0;
}

/* ── 示例问题卡片 ── */
.example-q {
    font-size: 0.78rem;
    color: var(--emerald-300) !important;
    padding: 0.3rem 0.65rem;
    border-left: 2px solid rgba(52,211,153,0.3);
    margin: 0.35rem 0;
    background: rgba(52,211,153,0.04);
    border-radius: 0 7px 7px 0;
    transition: background 0.2s;
}
.example-q:hover {
    background: rgba(52,211,153,0.08);
}

/* ── 空状态 ── */
.empty-state {
    text-align: center;
    padding: 3rem 0;
}
.empty-state .empty-icon {
    width: 56px; height: 56px;
    border-radius: 16px;
    background: var(--emerald-50);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    margin-bottom: 0.8rem;
}
.empty-state .empty-icon svg {
    width: 28px; height: 28px;
    stroke: var(--emerald-400);
}
.empty-state .empty-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--gray-600);
}
.empty-state .empty-desc {
    font-size: 0.82rem;
    color: var(--gray-400);
    margin-top: 0.3rem;
}
</style>
"""


def inject_css():
    """注入全局样式"""
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)


def page_header(title: str, desc: str, badge: str = "", icon: str = ""):
    """渲染页面头部横幅 (使用 SVG 图标)"""
    badge_html = f'<div class="badge">{badge}</div>' if badge else ""
    icon_html = svg_icon(icon, 28, "#ffffff") if icon else ""
    st.markdown(
        f'<div class="hero-header">'
        f'<h1>{icon_html}{title}</h1>'
        f'<div class="desc">{desc}</div>'
        f'{badge_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def section(title: str, icon_name: str = ""):
    """带 SVG 图标的区块标题"""
    if icon_name:
        icon_html = f'<div class="icon-box">{svg_icon(icon_name, 16, "#ffffff")}</div>'
    else:
        icon_html = ""
    st.markdown(
        f'<div class="section-head">{icon_html}'
        f'<div class="text">{title}</div></div>',
        unsafe_allow_html=True,
    )


def stat_card(icon_name: str, value: str, label: str, sub: str = ""):
    """数据指标卡片 (使用 SVG 图标)"""
    sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
    icon_html = f'<div class="stat-icon">{svg_icon(icon_name, 20, "currentColor")}</div>'
    st.markdown(
        f'<div class="stat-card">'
        f'{icon_html}'
        f'<div class="stat-value">{value}</div>'
        f'<div class="stat-label">{label}</div>'
        f'{sub_html}'
        f'</div>',
        unsafe_allow_html=True,
    )


def stat_card_row(cards: list):
    """一行多个指标卡片 — 使用 CSS Grid 保证等高。
    cards: list of (icon_name, value, label) 或 (icon_name, value, label, sub)
    """
    n = len(cards)
    htmls = []
    for c in cards:
        icon_name, value, label = c[0], c[1], c[2]
        sub = c[3] if len(c) > 3 else ""
        sub_html = f'<div class="stat-sub">{sub}</div>' if sub else ""
        icon_html = f'<div class="stat-icon">{svg_icon(icon_name, 20, "currentColor")}</div>'
        htmls.append(
            f'<div class="stat-card">'
            f'{icon_html}'
            f'<div class="stat-value">{value}</div>'
            f'<div class="stat-label">{label}</div>'
            f'{sub_html}'
            f'</div>'
        )
    st.markdown(
        f'<div class="stat-card-row" style="grid-template-columns:repeat({n},1fr);">'
        + "".join(htmls)
        + "</div>",
        unsafe_allow_html=True,
    )


def feature_card(icon_name: str, title: str, desc: str, tag: str, color_class: str):
    """首页功能模块卡片 (使用 SVG 图标)"""
    st.markdown(
        f'<div class="feature-card {color_class}">'
        f'<div class="fc-icon">{svg_icon(icon_name, 26, "currentColor")}</div>'
        f'<div class="fc-title">{title}</div>'
        f'<div class="fc-desc">{desc}</div>'
        f'<span class="fc-tag">{tag}</span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def feature_card_row(cards: list):
    """一行多个功能卡片 — 使用 CSS Grid 保证等高。
    cards: list of (icon_name, title, desc, tag, color_class)
    """
    n = len(cards)
    htmls = []
    for icon_name, title, desc, tag, color_class in cards:
        htmls.append(
            f'<div class="feature-card {color_class}">'
            f'<div class="fc-icon">{svg_icon(icon_name, 26, "currentColor")}</div>'
            f'<div class="fc-title">{title}</div>'
            f'<div class="fc-desc">{desc}</div>'
            f'<span class="fc-tag">{tag}</span>'
            f'</div>'
        )
    st.markdown(
        f'<div class="feature-card-row" style="grid-template-columns:repeat({n},1fr);">'
        + "".join(htmls)
        + "</div>",
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


def sidebar_brand():
    """侧边栏品牌区域 (共享组件)"""
    st.markdown(
        f'<div class="sidebar-brand">'
        f'<div class="brand-icon">{svg_icon("sprout", 26, "#ffffff")}</div>'
        f'<div class="brand-title">智慧农业预警系统</div>'
        f'<div class="brand-sub">Smart Agri Pest Warning</div>'
        f'</div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")


def sidebar_user(name: str = "系统管理员", role: str = "区域植保监控"):
    """侧边栏用户信息卡片"""
    st.markdown(
        f'<div class="sidebar-user">'
        f'<div class="avatar">{svg_icon("user", 18, "#ffffff")}</div>'
        f'<div><div class="name">{name}</div>'
        f'<div class="role">{role}</div></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def sidebar_footer(version: str = "v3.0"):
    """侧边栏底部版本信息"""
    st.markdown("---")
    st.markdown(
        f'<div class="sidebar-version">{version} &middot; Powered by XGBoost & DeepSeek</div>',
        unsafe_allow_html=True,
    )
