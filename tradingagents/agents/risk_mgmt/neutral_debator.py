import time
import json


def create_neutral_debator(llm):
    def neutral_node(state) -> dict:
        risk_debate_state = state["risk_debate_state"]
        history = risk_debate_state.get("history", "")
        neutral_history = risk_debate_state.get("neutral_history", "")

        current_risky_response = risk_debate_state.get("current_risky_response", "")
        current_safe_response = risk_debate_state.get("current_safe_response", "")

        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        trader_decision = state["trader_investment_plan"]

        prompt = f"""作为中性风险分析师，你的职责是提供平衡的观点，权衡交易员决定或计划的潜在收益和风险。你优先考虑全面的方法，评估上升和下降空间，同时考虑更广泛的市场趋势、潜在的经济变化和多元化策略。

**重要要求：你的所有分析和论证必须完全使用简体中文。**

以下是交易员的决定：

{trader_decision}

你的任务是挑战激进和安全分析师，指出每种观点可能过于乐观或过于谨慎的地方。利用以下数据源的见解来支持调整交易员决定的温和、可持续策略：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务报告：{news_report}
公司基本面报告：{fundamentals_report}
当前对话历史：{history} 激进分析师的最新回应：{current_risky_response} 安全分析师的最新回应：{current_safe_response}。如果其他观点没有回应，不要虚构，只需提出你的观点。

通过批判性地分析双方，解决激进和保守论点中的弱点来倡导更平衡的方法，积极参与。挑战他们的每个观点，说明为什么适度风险策略可能提供两全其美的效果，提供增长潜力同时防范极端波动。专注于辩论而不是简单地呈现数据，旨在表明平衡的观点可以带来最可靠的结果。以对话方式输出，就像你在说话一样，不使用任何特殊格式。"""

        response = llm.invoke(prompt)

        argument = f"Neutral Analyst: {response.content}"

        new_risk_debate_state = {
            "history": history + "\n" + argument,
            "risky_history": risk_debate_state.get("risky_history", ""),
            "safe_history": risk_debate_state.get("safe_history", ""),
            "neutral_history": neutral_history + "\n" + argument,
            "latest_speaker": "Neutral",
            "current_risky_response": risk_debate_state.get(
                "current_risky_response", ""
            ),
            "current_safe_response": risk_debate_state.get("current_safe_response", ""),
            "current_neutral_response": argument,
            "count": risk_debate_state["count"] + 1,
        }

        return {"risk_debate_state": new_risk_debate_state}

    return neutral_node
