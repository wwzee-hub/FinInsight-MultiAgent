import json
import re
from typing import List
from pydantic import BaseModel, Field
from config.settings import get_model


# 定义任务清单的结构
class Plan(BaseModel):
    steps: List[str] = Field(description="具体的调研步骤清单")


def planner_node(state):
    llm = get_model()
    # 强制要求 JSON 的 Prompt
    prompt = f"""你是一名调研规划师。请将调研“{state['task']}”拆解为3个搜索任务。
        必须只输出 JSON，格式如下：
        {{"steps": ["搜索任务1", "搜索任务2", "搜索任务3"]}}
        """

    response = llm.invoke(prompt)
    # response.content 是字符串
    content = response.content

    try:
        # 使用正则提取 JSON 部分，防止模型输出前言后语
        match = re.search(r"\{.*\}", content, re.DOTALL)
        if match:
            data = json.loads(match.group())
            return {"plan": data.get("steps", [])}
        else:
            # 如果没搜到 JSON 括号，尝试直接解析全文
            data = json.loads(content)
            return {"plan": data.get("steps", [])}
    except Exception as e:
        print(f"解析 JSON 出错，使用保底方案: {e}")
        return {"plan": [f"{state['task']} 市场分析", f"{state['task']} 财务数据", f"{state['task']} 竞争对手"]}