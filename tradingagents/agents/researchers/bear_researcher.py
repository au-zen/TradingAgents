from langchain_core.messages import AIMessage
import time
import json


def create_bear_researcher(llm, memory):
    def bear_node(state) -> dict:
        investment_debate_state = state["investment_debate_state"]
        history = investment_debate_state.get("history", "")
        bear_history = investment_debate_state.get("bear_history", "")

        current_response = investment_debate_state.get("current_response", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""你是一名看空分析师，负责论证不投资该股票的理由。你的目标是提出合理的论证，强调风险、挑战和负面指标。利用提供的研究和数据来突出潜在的不利因素并有效反驳看多论点。

**重要要求：你的所有分析和论证必须完全使用简体中文。**

重点关注以下方面：

- 风险和挑战：突出市场饱和、财务不稳定或宏观经济威胁等可能阻碍股票表现的因素。
- 竞争劣势：强调市场地位较弱、创新下降或来自竞争对手威胁等脆弱性。
- 负面指标：使用财务数据、市场趋势或最新不利新闻的证据来支持你的立场。
- 反驳看多观点：用具体数据和合理推理批判性分析看多论点，揭露弱点或过度乐观的假设。
- 参与辩论：以对话风格呈现你的论点，直接回应看多分析师的观点并进行有效辩论，而不仅仅是列举事实。

可用资源：

市场研究报告：{market_research_report}
社交媒体情绪报告：{sentiment_report}
最新世界事务新闻：{news_report}
公司基本面报告：{fundamentals_report}
辩论对话历史：{history}
最新看多论点：{current_response}
类似情况的反思和经验教训：{past_memory_str}
使用这些信息提出令人信服的看空论点，反驳看多声明，并参与动态辩论以展示投资该股票的风险和弱点。你还必须处理反思并从过去的经验教训和错误中学习。
"""

        response = llm.invoke(prompt)

        argument = f"Bear Analyst: {response.content}"

        new_investment_debate_state = {
            "history": history + "\n" + argument,
            "bear_history": bear_history + "\n" + argument,
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": argument,
            "count": investment_debate_state["count"] + 1,
        }

        return {"investment_debate_state": new_investment_debate_state}

    return bear_node
