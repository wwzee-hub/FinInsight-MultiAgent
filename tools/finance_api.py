import yfinance as yf


def fetch_finance_data(ticker: str):
    """
    获取指定股票代码（如 'TSLA', 'AAPL'）的财务摘要。
    """
    try:
        stock = yf.Ticker(ticker)
        # 获取基本信息
        info = stock.info
        summary = {
            "name": info.get("longName"),
            "current_price": info.get("currentPrice"),
            "market_cap": info.get("marketCap"),
            "pe_ratio": info.get("forwardPE"),
            "revenue_growth": info.get("revenueGrowth")
        }

        # 获取最新的季度财报摘要
        income_stmt = stock.quarterly_income_stmt.iloc[:, 0].to_dict()

        return {"summary": summary, "latest_financials": income_stmt}
    except Exception as e:
        return f"获取财务数据失败: {str(e)}"