"""数据加载与清洗模块"""
import pandas as pd
import numpy as np
from pathlib import Path
from utils.database import save_dataframe


DATA_DIR = Path(__file__).parent.parent / "data"


def generate_pest_history_data(n_records: int = 2000) -> pd.DataFrame:
    """
    生成模拟的历史病虫害数据
    
    实际项目中可从以下来源获取：
    - 全国农业技术推广服务中心 (www.natesc.org.cn) 的病虫害监测报告
    - 各省植保站公开数据
    - Kaggle农业数据集
    """
    np.random.seed(42)
    
    crops = ["水稻", "小麦", "玉米", "棉花", "大豆"]
    pests = {
        "水稻": ["稻飞虱", "稻纵卷叶螟", "二化螟", "纹枯病", "稻瘟病"],
        "小麦": ["蚜虫", "赤霉病", "条锈病", "白粉病", "纹枯病"],
        "玉米": ["玉米螟", "草地贪夜蛾", "大斑病", "小斑病", "锈病"],
        "棉花": ["棉铃虫", "蚜虫", "红蜘蛛", "枯萎病", "黄萎病"],
        "大豆": ["蚜虫", "食心虫", "根腐病", "霜霉病", "灰斑病"],
    }
    provinces = ["湖南", "湖北", "江西", "河南", "山东", "安徽", "四川", "黑龙江"]
    
    records = []
    for _ in range(n_records):
        crop = np.random.choice(crops)
        pest = np.random.choice(pests[crop])
        province = np.random.choice(provinces)
        month = np.random.randint(3, 11)  # 3-10月为主要种植季
        
        # 气象条件
        temperature = np.random.normal(20 + month * 1.5, 5)
        humidity = np.random.uniform(40, 95)
        rainfall = np.abs(np.random.exponential(8))
        
        # 病虫害严重程度受气象条件影响
        risk_score = (
            0.3 * (humidity / 100)
            + 0.2 * min(rainfall / 30, 1)
            + 0.2 * (1 - abs(temperature - 25) / 20)
            + 0.3 * np.random.uniform(0, 1)
        )
        risk_score = np.clip(risk_score, 0, 1)
        
        severity = (
            "轻度" if risk_score < 0.3
            else "中度" if risk_score < 0.6
            else "重度" if risk_score < 0.8
            else "特重"
        )
        
        records.append({
            "year": np.random.randint(2018, 2026),
            "month": month,
            "province": province,
            "crop": crop,
            "pest_name": pest,
            "temperature": round(temperature, 1),
            "humidity": round(humidity, 1),
            "rainfall": round(rainfall, 1),
            "risk_score": round(risk_score, 3),
            "severity": severity,
        })
    
    return pd.DataFrame(records)


def init_database():
    """初始化数据库，写入示例数据"""
    print("📦 正在生成模拟数据...")
    
    df = generate_pest_history_data(2000)
    save_dataframe(df, "pest_history")
    print(f"  ✅ pest_history: {len(df)} 条记录")
    
    # 生成作物-病虫害知识库
    knowledge = []
    pest_info = {
        "稻飞虱": {"crop": "水稻", "peak_month": "7-8月", "condition": "高温高湿", "prevention": "合理施肥，避免偏施氮肥；使用吡蚜酮等药剂"},
        "稻瘟病": {"crop": "水稻", "peak_month": "6-9月", "condition": "多雨寡照", "prevention": "选用抗病品种；发病初期喷施三环唑"},
        "草地贪夜蛾": {"crop": "玉米", "peak_month": "5-9月", "condition": "温暖地区全年", "prevention": "性诱剂监测，幼虫期施用氯虫苯甲酰胺"},
        "赤霉病": {"crop": "小麦", "peak_month": "4-5月", "condition": "花期遇雨", "prevention": "花期前后喷施戊唑醇、咪鲜胺"},
        "棉铃虫": {"crop": "棉花", "peak_month": "6-8月", "condition": "干旱少雨", "prevention": "利用赤眼蜂生物防治；Bt蛋白转基因品种"},
    }
    for name, info in pest_info.items():
        knowledge.append({"pest_name": name, **info})
    
    knowledge_df = pd.DataFrame(knowledge)
    save_dataframe(knowledge_df, "pest_knowledge")
    print(f"  ✅ pest_knowledge: {len(knowledge_df)} 条记录")
    
    print("🎉 数据库初始化完成！")


if __name__ == "__main__":
    init_database()
