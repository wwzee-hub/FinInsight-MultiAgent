from config.settings import get_model


def writer_node(state):
    llm = get_model(is_core=False)  # 这里可以用更快的配置

    prompt = f"""你是一名顶尖投行（如高盛、中金）的研报编辑器。
    你的任务是将下面的分析初稿转化为正式的行业研究报告。

    【初稿内容】:
    {state['draft']}

    【润色标准】:
    1. 保持专业、中立、理性的投行行文风格。
    2. 优化 Markdown 排版，使其层次分明，逻辑严密。
    3. 严禁删减初稿中的关键财务数据或事实。
    4. 纠正错别字和不通顺的句子。

    请直接输出润色后的研报全文："""

    response = llm.invoke(prompt)

    # 最终输出通常存储在 state 的不同 key 中，确保与 graph/state.py 一致
    return {"final_report": response.content}