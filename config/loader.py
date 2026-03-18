"""统一配置加载器 — 从 config.yaml 加载，自动解析环境变量引用"""
import os
import re
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

_CONFIG_PATH = Path(__file__).parent / "config.yaml"
_PROJECT_ROOT = Path(__file__).parent.parent
_config = None


def _resolve_env_vars(value):
    """递归解析 ${VAR_NAME} 和 ${VAR_NAME:default} 引用"""
    if isinstance(value, str):
        def _replace(match):
            var_name = match.group(1)
            default = match.group(3)
            return os.getenv(var_name, default if default is not None else "")
        return re.sub(r'\$\{([^}:]+)(:([^}]*))?\}', _replace, value)
    elif isinstance(value, dict):
        return {k: _resolve_env_vars(v) for k, v in value.items()}
    elif isinstance(value, list):
        return [_resolve_env_vars(item) for item in value]
    return value


def _resolve_db_path(cfg: dict) -> dict:
    """将 SQLite 相对路径转为基于项目根目录的绝对路径"""
    url = cfg.get("database", {}).get("url", "")
    if url.startswith("sqlite:///") and not url.startswith("sqlite:////"):
        # sqlite:///data/xxx.db → 提取相对路径部分
        rel_path = url[len("sqlite:///"):]
        abs_path = str((_PROJECT_ROOT / rel_path).resolve())
        cfg["database"]["url"] = f"sqlite:///{abs_path}"
    return cfg


def load_config() -> dict:
    """加载并缓存统一配置（全局单例）"""
    global _config
    if _config is not None:
        return _config
    with open(_CONFIG_PATH, "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f)
    _config = _resolve_env_vars(raw)
    _config = _resolve_db_path(_config)
    return _config


def get_active_llm() -> dict:
    """获取当前激活的 LLM 提供商配置，返回 {api_key, base_url, model}"""
    cfg = load_config()
    provider = cfg["llm"]["provider"]
    provider_cfg = cfg["llm"].get(provider)
    if not provider_cfg:
        raise ValueError(f"未找到 LLM 提供商配置: {provider}")
    return provider_cfg


def generate_datagen_yaml() -> str:
    """根据统一配置生成 DATAGEN agents YAML，返回文件路径"""
    cfg = load_config()
    llm = get_active_llm()

    agents = {}
    for name, opts in cfg.get("datagen", {}).get("agents", {}).items():
        agents[name] = {
            "provider": "openai",
            "model_config": {
                "model": llm["model"],
                "temperature": opts.get("temperature", 0.5),
                "openai_api_key": llm["api_key"],
                "openai_api_base": llm["base_url"],
            },
        }

    # 写到 DATAGEN 默认查找的路径: config/agent_models.yaml (相对于项目根目录)
    out_path = _PROJECT_ROOT / "config" / "agent_models.yaml"
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump({"agents": agents}, f, allow_unicode=True, default_flow_style=False)
    return str(out_path)


def generate_openchatbi_yaml() -> str:
    """根据统一配置生成 OpenChatBI YAML，返回文件路径"""
    cfg = load_config()
    llm = get_active_llm()
    ocbi = cfg.get("openchatbi", {})

    result = {
        "organization": ocbi.get("organization", ""),
        "dialect": ocbi.get("dialect", "sqlite"),
        "llm_providers": {
            "active": {
                "default_llm": {
                    "class": "langchain_openai.ChatOpenAI",
                    "params": {
                        "model": llm["model"],
                        "api_key": llm["api_key"],
                        "base_url": llm["base_url"],
                        "temperature": 0.3,
                    },
                }
            }
        },
        "default_llm": "active",
        "data_warehouse_config": {
            "type": "sqlite",
            "uri": cfg["database"]["url"],
        },
        "catalog_store": {
            "store_type": "file_system",
            "data_path": str(_PROJECT_ROOT / "data" / "catalog"),
        },
        "report_directory": ocbi.get("report_directory", "./reports"),
        "visualization_mode": ocbi.get("visualization_mode", "rule"),
        "python_executor": ocbi.get("python_executor", "restricted_local"),
    }

    out_path = Path(__file__).parent / ".generated" / "openchatbi_config.yaml"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        yaml.dump(result, f, allow_unicode=True, default_flow_style=False)
    return str(out_path)
