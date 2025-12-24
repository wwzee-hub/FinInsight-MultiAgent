# FinInsight-MultiAgent

**FinInsight-MultiAgent** 是一款专为金融从业者和行业研究员设计的全自动调研系统。本项目在 **1.5B** 参数量 的本地端侧模型（Qwen2.5）基础上，通过 **LangGraph** 编排多智能体协作流，实现了从“需求拆解 -> 实时检索 -> 深度分析 -> 合规审计 -> 专业润色”的全生命周期研报生成闭环。


## ✨ 核心特性

- **端侧轻量化部署**：针对 1.5B 小模型 进行深度调优。通过动态锚定（Dynamic Anchoring）和上下文限流策略，在不依赖高性能 GPU 和云端 API 的情况下，实现了逻辑严密的研报产出。
- **多智能体协同（Multi-Agent SOP）**：模仿投行研报生产流程，设计了 Planner、Researcher、Analyst、Critic、Writer 五大核心节点，各司其职。
- **防御性工程设计**：
  - **JSON 提取器**：针对小模型指令遵循度波动，开发了基于正则匹配的鲁棒性解析中间件。
  - **Token 熔断保护**：实现了数据流自动切片与清洗逻辑，有效预防长上下文导致的逻辑崩溃。
  - **循环审计机制：**：引入 Critic 节点进行自我修正，确保分析结果不偏离主题，降低幻觉率。
- **实时情报获取：**：集成 Tavily 搜索 API，赋予本地模型感知实时互联网动态的能力。


## 🏗️ 系统架构

本项目采用 **Stateful Graph（有状态图）** 架构，确保数据在不同 Agent 间流转的一致性：
1. **Planner (任务规划器)**：负责将调研目标分解为 3 个具体的搜索任务。

2. **Researcher (情报检索员)**：执行实时检索，并对万字原始数据进行预清洗与截断。

3. **Analyst (核心分析师)**：基于动态主题锚定技术，提取数据并进行金融逻辑归纳。

4. **Critic (合规审计师)**：对初稿进行逻辑审计，不达标则触发重写循环。

5. **Writer (研报排版员)**：执行最后的金融风格润色，输出标准 Markdown 研报。


## 🚀 快速开始

### 1. 环境准备
```bash
# 克隆仓库
git clone https://github.com/wwzee-hub/FinInsight-MultiAgent.git
cd FinInsight-MultiAgent

# 安装依赖
pip install -r requirements.txt
```

### 2. 模型配置
- 下载并启动 [Ollama](https://ollama.com/)。
- 拉取模型：```ollama run qwen2.5:1.5b```。

### 3. API 密钥
本项目使用 Tavily AI 作为搜索引擎，它是专为 LLM Agent 设计的搜索工具，你可以去 [Tavily AI 官网](https://tavily.com/) 申请一个```API Key```。
随后在根目录创建 .env 文件并填入：
```plaintext
TAVILY_API_KEY=your_tavily_api_key_here
```
### 4. 运行
```bash
python main.py
```
运行完成后，系统将在 data/reports/ 目录下生成专业研报。


## 🛠️ 技术架构
本项目采用了Agentic Workflow 模式，核心组件如下：

- **智能体编排 (Orchestration): LangGraph** (基于有状态图的编排，实现了 Critic-Loop 自动循环审计机制)。

- **核心框架: LangChain** (用于工具集成、Prompt 模版管理及链式调用)。

- **大语言模型 (LLM): Qwen2.5-1.5B** (通过 **Ollama** 本地私有化部署，实现低成本推理)。

- **外部搜索工具: Tavily AI API** (专为 LLM 设计的搜索引擎，提供高质量上下文抓取)。

- **数据流控制: Stateful Graph State** (基于类型注解的数据共享与累加机制)。

- **运行环境: Python 3.10+** (推荐使用 Conda 虚拟环境进行隔离)。


## 📂 项目结构
```plaintext
FinInsight-MultiAgent/
├── agents/                 # 核心 Agent 定义
│   ├── planner.py          # 任务拆解逻辑
│   ├── researcher.py       # 搜索与数据获取逻辑
│   ├── analyst.py          # 数据分析与逻辑撰写
│   ├── critic.py           # 审计与找茬逻辑
│   └── writer.py           # 最终排版润色
├── tools/                  # Agent 使用的工具箱
│   ├── finance_api.py      # 封装 Tushare Finance
│   ├── search_tool.py      # 封装 Tavily Search
│   └── chart_gen.py        # 调用 Matplotlib 生成图表
├── graph/                  # 编排层 (LangGraph 核心)
│   ├── state.py            # 定义 AgentState 结构
│   └── workflow.py         # 构建图节点、边、条件逻辑
├── prompts/                # 提示词管理 (解耦 Prompt 和代码)
│   ├── agent_prompts.yaml  # 所有的 System Prompt
│   └── templates.md        # 研报的 Markdown 模板
├── data/                   # 结果文件
│   └── reports/            # 生成的历史研报 MD
├── config/                 # 配置文件
│   └── settings.py         # API Keys, 模型参数配置
└── main.py                 # 程序入口
```


### 📜 许可证
本项目基于 MIT 许可证开源，详情请参见 [LICENSE](LICENSE) 文件。
