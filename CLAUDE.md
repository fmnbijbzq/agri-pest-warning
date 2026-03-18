# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Agricultural pest/disease warning system (智慧农业病虫害预警系统) — a Python web app combining XGBoost ML predictions, DeepSeek LLM analysis, and multi-agent orchestration to provide crop pest risk assessment for Chinese provinces.

## Environment

本项目使用 conda 环境 `agri-pest` 运行。所有命令均需在该环境下执行：

```bash
conda activate agri-pest
```

## Common Commands

```bash
# 激活环境
conda activate agri-pest

# Setup (first time)
bash scripts/setup.sh          # installs deps, clones DATAGEN, inits DB

# Or manual setup
pip install -r requirements.txt
cp .env.example .env           # then fill in DEEPSEEK_API_KEY
python models/data_loader.py   # initialize SQLite with sample data

# Run the app
streamlit run app/main.py

# Train/test the ML model standalone
python models/predictor.py
```

No test framework, linter, or CI is currently configured. The `tests/` directory exists but is empty.

## Architecture

### Data Flow

```
Weather data → Feature Engineering → XGBoost prediction → Risk score [0,1] → AI analysis (DeepSeek) → Dashboard
```

### Key Layers

- **Streamlit frontend** (`app/main.py` + `app/pages/`): 4 pages — data overview, risk warning map, AI chat assistant, report generation. Page files use emoji prefixes for Streamlit ordering (e.g. `1_📊_数据总览.py`).

- **Agent layer** (`agents/`): Abstract `BaseAgent` in `base.py` uses OpenAI-compatible client. Three concrete agents: `DataAgent` (NL2SQL), `PredictAgent` (ML inference), `ReportAgent` (markdown reports).

- **ML layer** (`models/`): `predictor.py` trains XGBRegressor, saves to `data/processed/risk_model.pkl`. `feature_engine.py` builds features (temp-humidity interaction, sin/cos seasonal encoding, one-hot for crop/province). `risk_evaluator.py` orchestrates weather + ML + LLM into a combined assessment.

- **Utilities** (`utils/`): `llm.py` wraps DeepSeek via OpenAI SDK with three modes (simple chat, data-aware chat, report gen). `database.py` handles SQLAlchemy operations against SQLite. `weather_api.py` provides mock weather data and Open-Meteo integration.

### External Dependencies

- **DATAGEN** (`external/DATAGEN/`): Cloned from GitHub by setup script. Multi-agent LangGraph workflow for automated research report generation. Configured via `config/datagen_agents.yaml`.
- **OpenChatBI**: pip package used for NL2SQL in the AI assistant page. Configured via `config/openchatbi_config.yaml`.

### LLM Integration

All LLM calls go through `utils/llm.py` → DeepSeek API using OpenAI-compatible interface. Provider is set by `LLM_PROVIDER` env var (default: `deepseek`). The `BaseAgent._chat()` method manages conversation history per agent instance.

## Configuration

- `config/settings.py`: Central config — API keys (from env), risk thresholds (low<0.3, medium<0.6, high<0.8), supported crops and provinces.
- `.env`: Required keys — `DEEPSEEK_API_KEY`. Optional — `DASHSCOPE_API_KEY`, `WEATHER_API_KEY`.
- `config/datagen_agents.yaml`: Maps 9 DATAGEN agent types to DeepSeek model with per-agent temperature.
- `config/openchatbi_config.yaml`: BM25 catalog store, SQLite connection, restricted Python executor.

## Database

SQLite at `data/agri_pest.db`. Main table is `pest_history` with columns for province, crop, month, weather metrics, pest type, severity, and risk_score. Initialized with synthetic data by `models/data_loader.py:init_database()`.
