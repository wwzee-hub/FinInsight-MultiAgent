from langgraph.graph import StateGraph, END
from agents.planner import planner_node
from agents.researcher import researcher_node
from agents.analyst import analyst_node
from agents.critic import critic_node
from agents.writer import writer_node
from graph.state import AgentState

# 1. 初始化图
workflow = StateGraph(AgentState)

# 2. 注册节点 (Nodes)
workflow.add_node("planner", planner_node)
workflow.add_node("researcher", researcher_node)
workflow.add_node("analyst", analyst_node)
workflow.add_node("critic", critic_node)
workflow.add_node("writer", writer_node)

# 3. 构建连线 (Edges)
workflow.set_entry_point("planner")
workflow.add_edge("planner", "researcher")
workflow.add_edge("researcher", "analyst")
workflow.add_edge("analyst", "critic")

# 4. 定义条件边 (Conditional Edges)
# 这个函数决定了从 Critic 节点出来后去哪里
def decide_next_step(state: AgentState):
    if state["finished"]:
        return "approved"
    else:
        # 如果没通过，可以回溯到 researcher 重新找资料，或者到 analyst 重新写
        return "retry"

workflow.add_conditional_edges(
    "critic",
    decide_next_step,
    {
        "approved": "writer",   # 审核通过 -> 润色
        "retry": "researcher"   # 审核失败 -> 重新搜索
    }
)

# 5. 完成最后的闭环
workflow.add_edge("writer", END)

# 6. 编译图
app = workflow.compile()