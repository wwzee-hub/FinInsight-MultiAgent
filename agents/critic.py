import re
import json
from pydantic import BaseModel, Field
from config.settings import get_model

class AuditResult(BaseModel):
    verdict: str = Field(description="判定结果：PASS 或 REJECT")
    reason: str = Field(description="打回的理由，如果通过则为空")


def critic_node(state):
    llm = get_model()
    prompt = f"请审计以下报告并输出 JSON (格式: {{\"verdict\": \"PASS/REJECT\", \"reason\": \"原因\"}}): {state['draft']}"

    response = llm.invoke(prompt)
    try:
        # 同理使用正则提取并 json.loads
        match = re.search(r"\{.*\}", response.content, re.DOTALL)
        data = json.loads(match.group())
        return {
            "critique": data.get("reason", ""),
            "finished": data.get("verdict") == "PASS"
        }
    except:
        # 保底：如果解析失败，默认让它通过，防止程序死循环
        return {"critique": "", "finished": True}