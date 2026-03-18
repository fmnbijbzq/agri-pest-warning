"""数据库操作封装"""
from sqlalchemy import create_engine, text
from config.settings import DATABASE_URL
import pandas as pd


engine = create_engine(DATABASE_URL)


def execute_query(sql: str) -> pd.DataFrame:
    """执行SQL查询，返回DataFrame"""
    with engine.connect() as conn:
        return pd.read_sql(text(sql), conn)


def save_dataframe(df: pd.DataFrame, table_name: str, if_exists: str = "replace"):
    """将DataFrame保存到数据库"""
    df.to_sql(table_name, engine, if_exists=if_exists, index=False)


def get_table_schema(table_name: str) -> str:
    """获取表结构信息，供NL2SQL使用"""
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table_name})"))
        columns = result.fetchall()
    schema_lines = [f"  {col[1]} {col[2]}" for col in columns]
    return f"表名: {table_name}\n字段:\n" + "\n".join(schema_lines)


def list_tables() -> list[str]:
    """列出所有数据表"""
    with engine.connect() as conn:
        result = conn.execute(text("SELECT name FROM sqlite_master WHERE type='table'"))
        return [row[0] for row in result.fetchall()]
