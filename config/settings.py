import os
from pathlib import Path
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama

# 加载 .env 文件（如果存在）
load_dotenv()


class Settings:
    # --- 1. 路径配置 ---
    BASE_DIR = Path(__file__).resolve().parent.parent
    PROMPT_DIR = BASE_DIR / "prompts"
    DATA_DIR = BASE_DIR / "data"
    REPORT_DIR = DATA_DIR / "reports"
    CHART_DIR = DATA_DIR / "charts"

    # --- 2. 模型切换开关 ---
    # 修改这里来决定使用本地还是云端
    USE_LOCAL = True  # True: 使用 Ollama, False: 使用 OpenAI

    # --- 3. 本地模型配置 (Ollama) ---
    OLLAMA_BASE_URL = "http://localhost:11434"
    OLLAMA_MODEL = "qwen2.5:1.5b"  # 确保你本地 ollama pull 了这个模型

    # --- 4. 云端模型配置 (OpenAI) ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-key-here")
    OPENAI_MODEL = "gpt-4o"

    # --- 5. 通用超参数 ---
    TEMPERATURE = 0.2
    MAX_RETRIES = 5  # 小模型逻辑弱，增加重试次数以提高成功率

    # --- 6. 工具配置 ---
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

    @classmethod
    def initialize_dirs(cls):
        """初始化项目所需的文件夹"""
        for _dir in [cls.DATA_DIR, cls.REPORT_DIR, cls.CHART_DIR]:
            _dir.mkdir(parents=True, exist_ok=True)


# 实例化
settings = Settings()
settings.initialize_dirs()


# --- 7. 模型工厂函数 (重点) ---

def get_model(is_core=True):
    """
    统一获取模型的函数。
    is_core: 是否是核心逻辑（Planner/Critic）。对于小模型，可以统一返回同一个。
    """
    if settings.USE_LOCAL:
        # 移除 with_structured_output 的依赖，只返回原始模型
        return ChatOllama(
            base_url=settings.OLLAMA_BASE_URL,
            model=settings.OLLAMA_MODEL,
            temperature=settings.TEMPERATURE
        )
    else:
        print(f"--- 使用云端模型: {settings.OPENAI_MODEL} ---")
        return ChatOpenAI(
            api_key=settings.OPENAI_API_KEY,
            model=settings.OPENAI_MODEL,
            temperature=settings.TEMPERATURE
        )