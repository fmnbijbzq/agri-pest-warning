"""风险综合评估模块"""
from models.predictor import predict_risk
from utils.weather_api import fetch_weather_mock
from utils.llm import chat_with_data


def evaluate_risk(province: str, crop: str, month: int = None) -> dict:
    """
    综合评估某地区某作物的病虫害风险
    整合气象数据 + ML预测 + AI分析
    """
    from datetime import datetime
    if month is None:
        month = datetime.now().month
    
    # 1. 获取近期气象数据
    weather_df = fetch_weather_mock(province, days=30)
    recent_weather = {
        "temperature": round(weather_df["temperature"].mean(), 1),
        "humidity": round(weather_df["humidity"].mean(), 1),
        "rainfall": round(weather_df["rainfall"].sum(), 1),
    }
    
    # 2. ML预测风险评分
    prediction = predict_risk({
        "month": month,
        "province": province,
        "crop": crop,
        **recent_weather,
    })
    
    # 3. AI生成分析建议
    data_context = (
        f"地区: {province}\n"
        f"作物: {crop}\n"
        f"月份: {month}月\n"
        f"近30天平均气温: {recent_weather['temperature']}℃\n"
        f"近30天平均湿度: {recent_weather['humidity']}%\n"
        f"近30天累计降雨: {recent_weather['rainfall']}mm\n"
        f"AI预测风险评分: {prediction['risk_score']}（{prediction['risk_level']}）\n"
    )
    
    ai_advice = chat_with_data(
        query=f"请分析{province}地区{crop}在{month}月的病虫害风险情况，并给出防治建议。",
        data_context=data_context,
    )
    
    return {
        "province": province,
        "crop": crop,
        "month": month,
        "weather": recent_weather,
        "prediction": prediction,
        "ai_advice": ai_advice,
    }
