"""全局配置 — 从统一配置 config.yaml 加载，保持原有接口不变"""
from config.loader import load_config

_cfg = load_config()
_llm = _cfg["llm"]

# LLM配置
LLM_PROVIDER = _llm["provider"]

DEEPSEEK_API_KEY = _llm.get("deepseek", {}).get("api_key", "")
DEEPSEEK_BASE_URL = _llm.get("deepseek", {}).get("base_url", "https://api.deepseek.com")
DEEPSEEK_MODEL = _llm.get("deepseek", {}).get("model", "deepseek-chat")

DASHSCOPE_API_KEY = _llm.get("dashscope", {}).get("api_key", "")

OPENAI_COMPATIBLE_BASE_URL = _llm.get("openai_compatible", {}).get("base_url", "")
OPENAI_COMPATIBLE_API_KEY = _llm.get("openai_compatible", {}).get("api_key", "")
OPENAI_COMPATIBLE_MODEL = _llm.get("openai_compatible", {}).get("model", "")

# 数据库
DATABASE_URL = _cfg["database"]["url"]

# 气象API
WEATHER_API_KEY = _cfg.get("weather", {}).get("api_key", "")

# 风险等级阈值
RISK_THRESHOLDS = _cfg["risk_thresholds"]

# 支持的作物类型
CROP_TYPES = _cfg["crops"]

# 支持的省份
PROVINCES = _cfg["provinces"]
