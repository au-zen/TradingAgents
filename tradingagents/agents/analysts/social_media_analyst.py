from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from langchain_core.tools import tool, BaseTool


def create_social_media_analyst(llm, toolkit):
    def social_media_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state.get("company_name", ticker)

        # Resolve official company name if still equals ticker
        if company_name == ticker:
            try:
                info_str = toolkit.get_stock_individual_info.invoke({"ticker": ticker})
                # Parse the company name from the returned string
                lines = info_str.split('\n')
                for line in lines:
                    if line.startswith("公司名称:"):
                        official_name = line.replace("公司名称:", "").strip()
                        if official_name:
                            state["company_name"] = official_name
                            company_name = official_name
                        break
            except Exception as e:
                # Keep original ticker as fallback
                pass

        def _toolize(fn):
            if isinstance(fn, BaseTool):
                return fn
            try:
                return tool(fn)
            except ValueError:
                return fn

        if toolkit.ticker_is_china_stock(ticker):
            base_funcs = [
                toolkit.get_stock_individual_info,
                toolkit.get_stock_zh_a_news,         # A股新闻（中文）
                # toolkit.get_stock_news_openai,     # 英文为主，暂时禁用
                # toolkit.get_google_news,           # 英文为主，暂时禁用
            ]
            tools = [_toolize(f) for f in base_funcs]
        elif toolkit.config["online_tools"]:
            tools = [_toolize(toolkit.get_stock_news_openai)]
        else:
            base_funcs = [toolkit.get_reddit_stock_info]
            tools = [_toolize(f) for f in base_funcs]

        system_message = (
            "你是一名顶级的社交媒体与情绪分析师，你的任务是为A股或美股撰写一份详细的舆情分析报告。"
            "请严格遵守以下要求："
            "1. **语言**: 报告必须完全使用简体中文。"
            "2. **公司识别**: 分析开始时，你的首要任务是调用 `get_stock_individual_info` 工具来获取公司的确切中文名称。在整个报告中，必须始终使用这个官方名称，而不是股票代码。"
            "3. **情绪分析**: 利用你拥有的工具集，分析与公司相关的新闻和社交媒体内容，以评估公众情绪。主要使用 `get_stock_news_openai` 和 `get_google_news` 工具。"
            "4. **报告结构**: 报告应首先总结整体的公众情绪（正面、负面或中性），然后提供具体的新闻和评论作为论据。最后，在报告的结尾处使用Markdown表格形式对关键发现和情绪趋势进行总结。"
            "5. **工具使用**: 你可用的工具有: {tool_names}。请根据任务需要选择最合适的工具。"
            "我们关注的股票代码是 **{ticker}**（{company_name}），当前分析日期是 **{current_date}**。"
        )

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(tool_names=", ".join([getattr(t, "name", getattr(t, "__name__", str(t))) for t in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(ticker=ticker)
        prompt = prompt.partial(company_name=company_name)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        report = ""

        if len(getattr(result, "tool_calls", [])) == 0:
            report = result.content

        return {
            "messages": [result],
            "sentiment_report": report,
        }
    return social_media_analyst_node
