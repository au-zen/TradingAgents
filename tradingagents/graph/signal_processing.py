# TradingAgents/graph/signal_processing.py

from langchain_openai import ChatOpenAI


class SignalProcessor:
    """Processes trading signals to extract actionable decisions."""

    def __init__(self, quick_thinking_llm: ChatOpenAI):
        """Initialize with an LLM for processing."""
        self.quick_thinking_llm = quick_thinking_llm

    def process_signal(self, full_signal: str) -> str:
        """
        Process a full trading signal to extract the core decision.

        Args:
            full_signal: Complete trading signal text

        Returns:
            Extracted decision (BUY, SELL, or HOLD)
        """
        messages = [
            (
                "system",
                "你是一名高效的助手，专门分析分析师团队提供的段落或财报。你的任务是用中文提取投资决策：买入、卖出或持有。只输出决策（买入、卖出或持有），不要添加任何额外内容。",
            ),
            ("human", full_signal),
        ]

        return self.quick_thinking_llm.invoke(messages).content
