from config.settings import get_model


def analyst_node(state):
    # 获取模型，is_core=True 表示使用较强的逻辑配置
    llm = get_model(is_core=True)

    # 1. 动态获取当前的调研主题（例如：小米汽车SU7）
    target_topic = state.get("task", "指定的行业/公司")

    # 2. 安全获取并处理原始数据
    all_data = state.get("raw_data", [])
    if not all_data:
        context_text = "（暂无搜索到的实时数据，请根据已知常识进行初步架构，但需注明数据缺失）"
    else:
        # 过滤非字符串并拼接
        clean_data = [str(d) for d in all_data if isinstance(d, str)]
        context_text = "\n---\n".join(clean_data)

    # 3. 针对 1.5B 小模型优化的动态锚定 Prompt
    prompt = f"""你是一名专门负责【{target_topic}】研究的资深行业分析师。

【严格准则】:
1. 你的分析必须且只能围绕“{target_topic}”展开。
2. 严禁输出“XX%”、“XX亿元”等模糊占位符。必须引用[原始数据]中的具体数值或事实。
3. 如果数据中没有提到某些信息，请直接说明“目前公开数据未显示”，严禁编造通用的行业废话（如全球数字化趋势等）。
4. 严禁原文照抄，需进行金融层面的逻辑归纳。

【参考原始数据】:
{context_text}

【任务】:
请撰写一份关于“{target_topic}”的深度调研初稿。

【写作结构】:
## 一、 {target_topic} 核心调研观点
### (此处分析其核心竞争力和市场地位)

## 二、 关键数据支撑与事实分析
### (此处列举数据中的具体参数、价格、交付量或技术细节)

## 三、 结论与潜在风险提示
### (根据数据给出结论)

请开始撰写报告："""

    # 调用模型
    response = llm.invoke(prompt)

    # 获取内容
    report_draft = response.content

    # 打印调试信息
    print(f"--- [Analyst 节点] 已完成对 {target_topic} 的分析，生成字数: {len(report_draft)} ---")

    return {"draft": report_draft}