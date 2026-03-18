#!/bin/bash
# ============================================================
# 项目初始化脚本 — 一键配置开发环境
# ============================================================

set -e
echo "🌾 智慧农业病虫害预警系统 — 环境初始化"
echo "============================================"

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_DIR"

# 1. 安装Python依赖
echo ""
echo "📦 [1/4] 安装Python依赖..."
pip install -r requirements.txt

# 2. 克隆DATAGEN（多Agent报告生成）
echo ""
echo "📦 [2/4] 克隆DATAGEN开源项目..."
mkdir -p external
if [ ! -d "external/DATAGEN" ]; then
    git clone --depth 1 https://github.com/starpig1129/DATAGEN.git external/DATAGEN
    echo "  ✅ DATAGEN克隆完成"
else
    echo "  ⏭ DATAGEN已存在，跳过"
fi

# 3. 配置环境变量
echo ""
echo "📦 [3/4] 检查环境变量..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "  ⚠️ 已创建.env文件，请编辑填入API Key:"
    echo "     vim .env"
else
    echo "  ✅ .env文件已存在"
fi

# 4. 初始化数据库
echo ""
echo "📦 [4/4] 初始化示例数据库..."
cd "$PROJECT_DIR"
python -c "
import sys
sys.path.insert(0, '.')
from models.data_loader import init_database
init_database()
"

echo ""
echo "============================================"
echo "🎉 初始化完成！"
echo ""
echo "启动应用:"
echo "  cd $PROJECT_DIR"
echo "  streamlit run app/main.py"
echo ""
echo "⚠️ 别忘了编辑 .env 填入 DEEPSEEK_API_KEY"
echo "============================================"
