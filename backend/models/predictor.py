"""ML预测模型 — 病虫害风险评分预测"""
import joblib
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, classification_report
from xgboost import XGBRegressor, XGBClassifier

from models.feature_engine import build_features, get_feature_columns
from utils.database import execute_query

MODEL_DIR = Path(__file__).parent.parent / "data" / "processed"


def train_risk_model() -> dict:
    """训练风险评分回归模型"""
    df = execute_query("SELECT * FROM pest_history")
    features = build_features(df)
    feature_cols = get_feature_columns(features)
    
    X = features[feature_cols].values
    y = features["risk_score"].values
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = XGBRegressor(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        random_state=42,
    )
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    metrics = {
        "rmse": round(np.sqrt(mean_squared_error(y_test, y_pred)), 4),
        "r2": round(r2_score(y_test, y_pred), 4),
    }
    
    # 保存模型
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    model_path = MODEL_DIR / "risk_model.pkl"
    joblib.dump({"model": model, "feature_cols": feature_cols}, model_path)
    
    print(f"✅ 模型训练完成: RMSE={metrics['rmse']}, R²={metrics['r2']}")
    print(f"   模型已保存到: {model_path}")
    return metrics


def predict_risk(input_data: dict) -> dict:
    """
    预测病虫害风险
    
    input_data示例:
    {
        "month": 7,
        "province": "湖南",
        "crop": "水稻",
        "temperature": 28.5,
        "humidity": 85.0,
        "rainfall": 12.3,
    }
    """
    model_path = MODEL_DIR / "risk_model.pkl"
    if not model_path.exists():
        train_risk_model()
    
    saved = joblib.load(model_path)
    model = saved["model"]
    feature_cols = saved["feature_cols"]
    
    # 构建输入DataFrame
    input_df = pd.DataFrame([input_data])
    features = build_features(input_df)
    
    # 确保列对齐
    for col in feature_cols:
        if col not in features.columns:
            features[col] = 0
    
    X = features[feature_cols].values
    risk_score = float(model.predict(X)[0])
    risk_score = np.clip(risk_score, 0, 1)
    
    # 风险等级
    if risk_score < 0.3:
        level, color = "低风险", "green"
    elif risk_score < 0.6:
        level, color = "中风险", "orange"
    elif risk_score < 0.8:
        level, color = "高风险", "red"
    else:
        level, color = "极高风险", "darkred"
    
    return {
        "risk_score": round(risk_score, 3),
        "risk_level": level,
        "color": color,
        "input": input_data,
    }


if __name__ == "__main__":
    metrics = train_risk_model()
    
    # 测试预测
    result = predict_risk({
        "month": 7, "province": "湖南", "crop": "水稻",
        "temperature": 30, "humidity": 90, "rainfall": 20,
    })
    print(f"\n预测结果: {result}")
