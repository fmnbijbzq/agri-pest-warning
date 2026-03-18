"""气象数据获取工具"""
import requests
import pandas as pd
from datetime import datetime, timedelta


def fetch_weather_mock(province: str, days: int = 30) -> pd.DataFrame:
    """
    获取气象数据（模拟版本）
    
    实际项目中可对接：
    - 中国气象数据网 (data.cma.cn) 
    - 和风天气API (qweather.com) — 有免费额度
    - Open-Meteo API (open-meteo.com) — 完全免费
    """
    import numpy as np
    np.random.seed(42)
    
    dates = [datetime.now() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    data = {
        "date": dates,
        "province": province,
        "temperature": np.random.normal(22, 8, days).round(1),          # 平均气温 ℃
        "humidity": np.random.uniform(40, 95, days).round(1),            # 湿度 %
        "rainfall": np.abs(np.random.exponential(5, days)).round(1),     # 降雨量 mm
        "wind_speed": np.random.uniform(0.5, 8, days).round(1),         # 风速 m/s
        "sunshine_hours": np.random.uniform(2, 12, days).round(1),      # 日照时数
    }
    return pd.DataFrame(data)


def fetch_weather_openmeteo(lat: float, lon: float, days: int = 30) -> pd.DataFrame:
    """
    通过Open-Meteo API获取真实气象数据（免费，无需API Key）
    文档: https://open-meteo.com/en/docs
    """
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "daily": "temperature_2m_mean,relative_humidity_2m_mean,precipitation_sum,wind_speed_10m_max,sunshine_duration",
        "timezone": "Asia/Shanghai",
    }
    
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()["daily"]
    
    df = pd.DataFrame({
        "date": pd.to_datetime(data["time"]),
        "temperature": data["temperature_2m_mean"],
        "humidity": data["relative_humidity_2m_mean"],
        "rainfall": data["precipitation_sum"],
        "wind_speed": data["wind_speed_10m_max"],
        "sunshine_hours": [d / 3600 for d in data["sunshine_duration"]],  # 秒→小时
    })
    return df


# 主要城市经纬度（用于Open-Meteo查询）
CITY_COORDS = {
    "长沙": (28.23, 112.94), "武汉": (30.58, 114.27), "南昌": (28.68, 115.86),
    "合肥": (31.82, 117.23), "南京": (32.06, 118.80), "杭州": (30.25, 120.17),
    "成都": (30.57, 104.07), "郑州": (34.75, 113.65), "济南": (36.65, 116.98),
    "广州": (23.13, 113.26), "昆明": (25.04, 102.68), "哈尔滨": (45.75, 126.65),
}
