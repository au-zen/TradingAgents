from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import time
import json
from langchain_core.tools import tool
from ..utils.tool_validation import ToolCallValidator, enhance_system_message_with_validation


def create_fundamentals_analyst(llm, toolkit):
    def fundamentals_analyst_node(state):
        current_date = state["trade_date"]
        ticker = state["company_of_interest"]
        company_name = state.get("company_name", ticker)

        # Try to resolve official company name if still equals ticker
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

        from langchain_core.tools import BaseTool
        def _toolize(fn):
            if isinstance(fn, BaseTool):
                return fn
            try:
                return tool(fn)
            except ValueError:
                return fn

        if toolkit.ticker_is_china_stock(ticker):
            # A股工具配置 - 优先级最高
            base_funcs = [
                toolkit.get_stock_individual_info,   # 获取公司信息
                toolkit.get_fundamentals,     # 财报
                toolkit.get_stock_report,            # 分析师报告
                toolkit.get_stock_cg_lg,             # 机构持仓
                toolkit.get_stock_dzjy_detail,       # 大宗交易
            ]
            tools = [_toolize(f) for f in base_funcs]
        elif toolkit.config["online_tools"]:
            # 美股在线工具配置
            tools = [_toolize(toolkit.get_fundamentals)]
        else:
            # 美股离线工具配置
            base_funcs = [
                toolkit.get_finnhub_company_insider_sentiment,
                toolkit.get_finnhub_company_insider_transactions,
                toolkit.get_simfin_balance_sheet,
                toolkit.get_simfin_cashflow,
                toolkit.get_simfin_income_stmt,
            ]
            tools = [_toolize(f) for f in base_funcs]

        base_system_message = (
            "你是一名严谨的公司基本面分析师，你的任务是基于工具提供的数据，为A股或美股撰写一份详细、准确的基本面分析报告。"
            "**重要要求：你的所有分析和报告必须完全使用简体中文。**"
            "**绝对禁止**在没有工具数据支持的情况下编造任何信息。如果工具没有返回数据，请明确说明'无法获取相关数据'。"
            "请严格遵循以下步骤："
            "1. **识别公司**: 这是你的第一步，也是最重要的一步。立即调用 `get_stock_individual_info` 工具，使用 `{ticker}` 作为参数，获取公司的官方中文全称。在获得公司名称之前，**不得**进行任何其他分析或生成任何文本。"
            "2. **数据采集**: 获取公司名称后，使用可用的财务工具（如 `get_fundamentals`、`get_stock_report` 等）获取该公司的核心财务数据和基本面信息。你必须使用从第一步获得的官方公司名称进行后续分析。"
            "3. **撰写报告**: 仅使用上述工具返回的真实数据撰写报告。报告必须完全使用简体中文。报告内容应包括对公司财务状况、优势、劣势和潜在风险的客观评估，并在结尾处使用Markdown表格进行总结。"
            "4. **数据验证**: 在报告中明确标注数据来源，如果某项数据无法获取，请明确说明。"
            "5. **工具列表**: 你可用的工具有: {tool_names}。"
            "我们关注的股票代码是 **{ticker}**，当前分析日期是 **{current_date}**。"
            "公司名称（如已获取）: **{company_name}**"
        )

        # 增强系统消息，添加数据验证要求
        system_message = enhance_system_message_with_validation(base_system_message)

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )
        prompt = prompt.partial(tool_names=", ".join([getattr(t, "name", getattr(t, "__name__", str(t))) for t in tools]))
        prompt = prompt.partial(current_date=current_date)
        prompt = prompt.partial(company_name=company_name)
        prompt = prompt.partial(ticker=ticker)

        chain = prompt | llm.bind_tools(tools)

        result = chain.invoke(state["messages"])

        # 创建工具调用验证器
        validator = ToolCallValidator()

        # 验证工具调用
        validation_result = validator.validate_tool_calls([result])

        report = ""

        if len(getattr(result, "tool_calls", [])) == 0:
            report = result.content

            # 如果没有工具调用但包含可疑内容，添加警告
            if not validation_result["valid"]:
                report += "\n\n⚠️ **数据验证警告**: 此报告可能包含不准确的信息，建议重新生成。"

        return {
            "messages": [result],
            "fundamentals_report": report,
        }
    return fundamentals_analyst_node
