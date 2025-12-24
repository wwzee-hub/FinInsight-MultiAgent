import operator
from typing import Annotated, List, TypedDict

def merge_lists(left: list, right: list) -> list:
    """用于合并列表的 reducer 函数"""
    return left + right


class AgentState(TypedDict):
    # 用户原始输入
    task: str

    # Planner 生成的任务清单
    plan: List[str]

    # Researcher 搜集的原始信息 (Annotated 配合 merge_lists 可以累加搜索结果)
    raw_data: Annotated[List[str], operator.add]

    # Analyst 写的报告初稿
    draft: str

    # Critic 提供的修改意见
    critique: str

    # 状态控制：是否完成审核
    finished: bool

    # 最终输出的报告内容
    final_report: str