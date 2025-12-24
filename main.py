import sys
import os
from datetime import datetime

# 确保项目根目录在路径中，防止导入错误
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from graph.workflow import app
from config.settings import settings


def print_separator(title):
    print(f"\n{'=' * 20} {title} {'=' * 20}")


def run_fin_agent():
    # 1. 初始化目录
    settings.initialize_dirs()

    print_separator("FinInsight Multi-Agent System")
    if settings.USE_LOCAL:
        print(f"模式: [本地推理] | 模型: {settings.OLLAMA_MODEL}")
    else:
        print(f"模式: [云端API] | 模型: {settings.OPENAI_MODEL}")

    # 2. 获取用户输入
    user_input = input("\n请输入你想调研的公司或行业方向 (例如: 小米汽车SU7): ")

    # 3. 构建初始状态
    # 匹配 graph/state.py 中的 AgentState 定义
    initial_state = {
        "task": user_input,
        "plan": [],
        "raw_data": [],
        "draft": "",
        "critique": "",
        "finished": False,
        "revision_count": 0
    }

    # 4. 运行 LangGraph 工作流
    print_separator("开始执行任务流")
    final_state = {}

    # 使用 stream 模式实时查看每个节点的产出
    try:
        for event in app.stream(initial_state):
            for node_name, output in event.items():
                print(f"\n[节点: {node_name}] 执行完毕")
                final_state.update(output)

                # 根据不同节点打印关键信息，方便调试
                if node_name == "planner":
                    print(f"📋 任务拆解完成: {output.get('plan', [])}")
                elif node_name == "researcher":
                    raw_data_list = output.get('raw_data', [])
                    actual_content = "".join(raw_data_list)
                    print(f"🔍 数据搜集完成，字数: {len(actual_content)}")
                elif node_name == "critic":
                    verdict = "✅ 通过" if output.get("finished") else "❌ 打回重做"
                    print(f"⚖️ 审计结论: {verdict}")
                    if not output.get("finished"):
                        print(f"💡 修改建议: {output.get('critique')}")
                elif node_name == "writer":
                    print(f"📝 最终研报已生成！")

        # 5. 任务结束，保存结果
        # 这里假设最后一步是生成了 final_report 或在 draft 中
        # 你可以从最后一次迭代的 state 中提取内容
        print_separator("任务成功结束")
        # 获取最终报告内容 (优先取 final_report，没有则取 draft)
        report_content = final_state.get("final_report") or final_state.get("draft")

        if report_content:
            # 生成文件名：小米汽车SU7_20240321.md
            safe_name = user_input.replace(" ", "_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{safe_name}_{timestamp}.md"
            filepath = os.path.join(settings.REPORT_DIR, filename)

            # 写入文件
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(report_content)

            print(f"✅ 研报已成功保存至: {filepath}")
        else:
            print("⚠️ 警告：未找到生成的研报内容，无法保存。")

    except Exception as e:
        print(f"\n程序运行出错: {e}")
        print("提示: 请检查 Ollama 是否已启动，且模型已拉取。")


if __name__ == "__main__":
    run_fin_agent()