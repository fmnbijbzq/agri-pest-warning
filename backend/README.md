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
- **可视化**: Plotly, ECharts (pyecharts)

## 项目结构

```
agri-pest-warning/
├── README.md                 # 项目说明
├── requirements.txt          # Python依赖
├── .env.example              # 环境变量模板
├── config/
│   └── settings.py           # 全局配置
├── data/
│   ├── raw/                  # 原始数据
│   └── processed/            # 处理后数据
├── app/
│   ├── main.py               # Streamlit主页面
│   ├── pages/
│   │   ├── 1_数据总览.py      # 数据展示页
│   │   ├── 2_风险预警.py      # 预警地图页
│   │   ├── 3_AI助手.py       # AI对话页
│   │   └── 4_分析报告.py      # 报告生成页
│   └── components/
│       ├── charts.py         # 图表组件
│       └── sidebar.py        # 侧边栏组件
├── agents/
│   ├── __init__.py
│   ├── base.py               # Agent基类
│   ├── data_agent.py         # 数据分析Agent
│   ├── predict_agent.py      # 预测预警Agent
│   └── report_agent.py       # 报告生成Agent
├── models/
│   ├── __init__.py
│   ├── data_loader.py        # 数据加载与清洗
│   ├── feature_engine.py     # 特征工程
│   ├── predictor.py          # ML预测模型
│   └── risk_evaluator.py     # 风险评估
├── utils/
│   ├── __init__.py
│   ├── llm.py                # 大模型调用封装
│   ├── database.py           # 数据库操作
│   └── weather_api.py        # 气象数据API
├── tests/
│   └── test_predictor.py     # 单元测试
└── docs/
    └── 研究报告模板.md         # 比赛研究报告模板
```

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env 填入 DeepSeek API Key

# 3. 初始化示例数据
python models/data_loader.py

# 4. 启动应用
streamlit run app/main.py
```

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
- [nl2sql_agent](https://github.com/xifanz42/nl2sql_agent) — NL2SQL交互模块
- [OpenChatBI](https://github.com/zhongyu09/openchatbi) — 对话式BI平台
