def researcher_node(state):
    from tools.search_tool import search_online

    plan = state.get("plan", [])
    all_raw_results = []

    print(f"--- Researcher 开始检索 ---")

    for task in plan:
        # 实际调用搜素引擎
        search_res = search_online(task)
        # 将结果转为字符串并清洗多余空格
        cleaned_res = str(search_res).replace("\n", " ").strip()
        all_raw_results.append(cleaned_res)

    # 将所有结果合并
    combined_data = " ".join(all_raw_results)

    max_chars = 20000
    if len(combined_data) > max_chars:
        print(f"⚠️ 数据过长 ({len(combined_data)}字)，已截断至 {max_chars} 字以防模型崩溃")
        combined_data = combined_data[:max_chars] + "...[数据过长已截断]"

    return {"raw_data": [combined_data]}