# 🌾 智慧农业病虫害预警系统

> 基于大数据与AI Agent的农作物病虫害智能预警平台

## 项目简介

本项目利用公开气象数据、土壤数据和历史病虫害记录，结合机器学习预测模型与AI Agent智能分析，
为农业工作者提供病虫害风险预警和防治建议。

## 技术栈

- **后端**: Python 3.11+
- **数据处理**: Pandas, NumPy
- **机器学习**: Scikit-learn, XGBoost
- **AI Agent**: LangChain + DeepSeek API（国产大模型）
- **数据库**: SQLite（开发）/ PostgreSQL（生产）
- **前端**: Streamlit
- **可视化**: Plotly, Folium (GIS地图)
- **GIS集成**: Folium + streamlit-folium（历史病虫害时空溯源）

## 项目结构

```
backend/
├── README.md                 # 项目说明
├── requirements.txt          # Python依赖
├── .env.example              # 环境变量模板
├── .streamlit/
│   └── config.toml           # Streamlit主题与服务配置
├── config/
│   ├── settings.py           # 全局配置（API Key、风险阈值、作物列表等）
│   └── loader.py             # YAML/环境变量加载器
├── data/
│   ├── agri_pest.db          # SQLite 数据库
│   ├── raw/                  # 原始数据
│   └── processed/            # 处理后数据与模型文件
├── app/
│   ├── 🏠_首页.py             # Streamlit 主入口页面
│   ├── ui_style.py           # 全局 CSS 设计系统
│   └── pages/
│       ├── 1_📈_数据总览.py   # 数据可视化（Plotly图表）
│       ├── 2_⚠️_风险预警.py    # XGBoost风险预测与预警
│       ├── 3_💬_AI助手.py     # AI对话（OpenChatBI / NL2SQL）
│       ├── 4_📄_分析报告.py   # 多Agent协作报告生成
│       └── 5_🌍_GIS溯源.py   # 历史病虫害GIS地图可视化
├── agents/
│   ├── base.py               # Agent基类（OpenAI兼容客户端）
│   ├── data_agent.py         # 数据分析Agent（NL2SQL）
│   ├── predict_agent.py      # 预测预警Agent
│   ├── report_agent.py       # 报告生成Agent
│   ├── chatbi_integration.py # OpenChatBI 集成适配
│   └── datagen_integration.py# DATAGEN 多Agent集成
├── models/
│   ├── data_loader.py        # 数据加载与数据库初始化
│   ├── feature_engine.py     # 特征工程（温湿交互、季节编码等）
│   ├── predictor.py          # XGBoost 模型训练与预测
│   └── risk_evaluator.py     # 风险综合评估（气象+ML+LLM）
├── utils/
│   ├── llm.py                # DeepSeek 大模型调用封装
│   ├── database.py           # SQLAlchemy 数据库操作
│   └── weather_api.py        # 气象数据API（Open-Meteo + Mock）
├── external/
│   ├──  openchatbi           # 智能聊天型 BI 工具(git clone)
│   └── DATAGEN/              # 多Agent研究报告框架（git clone）
├── tests/                    # 测试目录
└── docs/                     # 文档
```

## 快速开始

### 1. 创建 Conda 环境

```bash
conda create -n agri-pest python=3.11 -y
conda activate agri-pest
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 填入 DeepSeek API Key
```

### 4. 初始化数据库

```bash
python models/data_loader.py
```

### 5. 启动应用

```bash
streamlit run app/🏠_首页.py
```

## 依赖说明

| 类别 | 包名 | 用途 |
|------|------|------|
| **核心** | pandas, numpy | 数据处理与数值计算 |
| **ML** | scikit-learn, xgboost, joblib | 风险预测模型训练与推理 |
| **AI/LLM** | openai, langchain, langgraph | DeepSeek API调用与Agent编排 |
| **NL2SQL** | openchatbi | AI助手自然语言数据库查询 |
| **DATAGEN核心** | langchain-anthropic, langchain-google-genai, langchain-ollama, langchain-groq, mcp | DATAGEN多LLM提供商支持与MCP协议 |
| **DATAGEN工具链** | selenium, arxiv, beautifulsoup4, wikipedia, firecrawl-py | 网页搜索、论文检索、网页爬取解析 |
| **前端** | streamlit, plotly | Web界面与图表可视化 |
| **GIS** | folium, streamlit-folium | 地图可视化与热力图 |
| **数据库** | sqlalchemy | SQLite ORM操作 |
| **配置** | python-dotenv, pyyaml | 环境变量与YAML配置加载 |
| **网络** | requests | 气象API数据获取 |
| **检索** | faiss-cpu | 向量相似度检索 |

## AI工具使用说明（比赛合规）

本项目使用以下大赛指定AI工具：
- **DeepSeek** — 自然语言交互、数据分析、报告生成
- **通义千问（备选）** — 可通过配置切换

## 团队分工建议

| 角色 | 人数 | 负责模块 |
|------|------|---------|
| 数据工程 | 1人 | data/, models/data_loader, models/feature_engine |
| ML建模 | 1人 | models/predictor, models/risk_evaluator |
| AI Agent开发 | 1人 | agents/, utils/llm |
| 前端展示 | 1人 | app/ |

## 参考项目

- [DATAGEN](https://github.com/starpig1129/DATAGEN) — 多Agent研究助手架构
- [OpenChatBI](https://github.com/fmnbijbzq/openchatbi) — 对话式BI平台
