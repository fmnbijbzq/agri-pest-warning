"""特征工程模块"""
import pandas as pd
import numpy as np


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """从原始数据构建ML特征"""
    features = df.copy()
    
    # 温湿度交互特征（高温高湿易爆发病虫害）
    features["temp_humidity_index"] = features["temperature"] * features["humidity"] / 100
    
    # 月份编码（用正弦/余弦保留周期性）
    features["month_sin"] = np.sin(2 * np.pi * features["month"] / 12)
    features["month_cos"] = np.cos(2 * np.pi * features["month"] / 12)
    
    # 降雨分级
    features["rain_level"] = pd.cut(
        features["rainfall"],
        bins=[-np.inf, 5, 15, 30, np.inf],
        labels=[0, 1, 2, 3],
    ).astype(int)
    
    # 作物one-hot编码
    crop_dummies = pd.get_dummies(features["crop"], prefix="crop")
    features = pd.concat([features, crop_dummies], axis=1)
    
    # 省份one-hot编码
    province_dummies = pd.get_dummies(features["province"], prefix="prov")
    features = pd.concat([features, province_dummies], axis=1)
    
    return features


def get_feature_columns(df: pd.DataFrame) -> list[str]:
    """返回用于模型训练的特征列名"""
    exclude = ["year", "pest_name", "severity", "risk_score", "crop", "province"]
    return [c for c in df.columns if c not in exclude]
