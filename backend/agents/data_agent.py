"""数据分析Agent — 自然语言查询数据库（参考nl2sql_agent）"""
from agents.base import BaseAgent
from utils.database import execute_query, get_table_schema, list_tables

NL2SQL_SYSTEM = """你是一个专业的SQL生成助手。根据用户的自然语言问题，生成对应的SQLite SQL查询。

数据库表结构：
{schema}

规则：
1. 只生成SELECT查询，不允许修改数据
2. 只输出SQL语句，不要解释
3. SQL用```sql```包裹
"""


class DataAgent(BaseAgent):
    """数据分析Agent：自然语言→SQL→执行→自然语言解读"""
    
    def __init__(self):
        super().__init__(
            name="数据分析Agent",
            description="通过自然语言查询和分析农业病虫害数据",
        )
    
    def run(self, input_data: dict) -> dict:
        query = input_data.get("query", "")
        
        # 1. 获取数据库schema
        tables = list_tables()
        schemas = "\n\n".join(get_table_schema(t) for t in tables)
        
        # 2. NL → SQL
        system = NL2SQL_SYSTEM.format(schema=schemas)
        sql_response = self._chat(query, system=system)
        
        # 提取SQL
        sql = self._extract_sql(sql_response)
        if not sql:
            return {"error": "无法生成SQL", "raw": sql_response}
        
        # 3. 执行SQL
        try:
            df = execute_query(sql)
            result_text = df.to_string(index=False, max_rows=20)
        except Exception as e:
            return {"error": f"SQL执行失败: {e}", "sql": sql}
        
        # 4. AI解读结果
        interpretation = self._chat(
            f"以下是查询结果，请用中文简要解读：\n\n查询: {query}\nSQL: {sql}\n结果:\n{result_text}",
            system="你是农业数据分析师，请用通俗易懂的语言解读数据查询结果。",
        )
        
        return {
            "query": query,
            "sql": sql,
            "data": df.to_dict(orient="records"),
            "interpretation": interpretation,
        }
    
    @staticmethod
    def _extract_sql(text: str) -> str:
        """从AI回复中提取SQL语句"""
        if "```sql" in text:
            return text.split("```sql")[1].split("```")[0].strip()
        if "```" in text:
            return text.split("```")[1].split("```")[0].strip()
        return text.strip()
