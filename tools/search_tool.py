from langchain_community.tools.tavily_search import TavilySearchResults

def get_web_search_tool():
    """
    配置并返回 Tavily 搜索工具。
    需要在环境变量中设置 TAVILY_API_KEY
    """
    # k=5 表示搜索返回前5条最相关的结果
    return TavilySearchResults(k=5)

def search_online(query: str):
    search = get_web_search_tool()
    results = search.run(query)
    return results