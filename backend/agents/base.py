"""Agent基类 — 参考DATAGEN的多Agent架构"""
from abc import ABC, abstractmethod
from utils.llm import get_llm_client


class BaseAgent(ABC):
    """所有Agent的基类"""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.client, self.model = get_llm_client()
        self.history: list[dict] = []
    
    @abstractmethod
    def run(self, input_data: dict) -> dict:
        """执行Agent任务"""
        pass
    
    def _chat(self, prompt: str, system: str = "") -> str:
        """内部对话方法"""
        messages = [{"role": "system", "content": system}] if system else []
        messages.extend(self.history)
        messages.append({"role": "user", "content": prompt})
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.3,
        )
        
        reply = response.choices[0].message.content
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": reply})
        return reply
    
    def reset(self):
        """清空对话历史"""
        self.history = []
