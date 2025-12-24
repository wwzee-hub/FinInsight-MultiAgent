import matplotlib.pyplot as plt
import os

def generate_comparison_chart(labels: list, values: list, title: str, filename: str):
    """
    根据 Agent 提取的数据生成柱状图并保存。
    """
    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color=['blue', 'green', 'orange', 'red'])
    plt.title(title)
    plt.ylabel('数值')

    # 确保保存路径存在
    output_dir = "data/charts"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    save_path = os.path.join(output_dir, f"{filename}.png")
    plt.savefig(save_path)
    plt.close()

    return f"图表已生成并保存至: {save_path}"