import pytest
from unittest.mock import Mock, MagicMock
import datetime

@pytest.fixture
def mock_console():
    """Provide a mocked rich console instance."""
    return Mock()

@pytest.fixture
def mock_typer():
    """Provide a mocked typer instance."""
    return Mock()

@pytest.fixture
def sample_selections():
    """Provide sample user selections data."""
    return {
        "ticker": "603127.SH",
        "analysis_date": datetime.datetime.now().strftime("%Y-%m-%d"),
        "analysts": ["market", "social", "news", "fundamentals"],
        "research_depth": "shallow",
        "llm_provider": "openrouter",
        "backend_url": "https://openrouter.ai/api/v1",
        "shallow_thinker": "DeepSeek V3",
        "deep_thinker": "DeepSeek V3"
    }

@pytest.fixture
def sample_state_data():
    """Provide sample analysis state data."""
    return {
        "market_report": "# Market Analysis\nPositive market trends observed...",
        "sentiment_report": "# Sentiment Analysis\nOverall positive sentiment...",
        "news_report": "# News Analysis\nRecent developments indicate...",
        "fundamentals_report": "# Fundamentals Analysis\nStrong financial indicators...",
        "investment_debate_state": {
            "bull_history": "Bullish case based on growth prospects...",
            "bear_history": "Bearish concerns about market conditions...",
            "judge_decision": "Balanced view considering both perspectives..."
        },
        "trader_investment_plan": "# Trading Strategy\nRecommend gradual position building...",
        "risk_debate_state": {
            "risky_history": "High potential returns identified...",
            "safe_history": "Conservative approach suggested...",
            "neutral_history": "Balanced risk assessment...",
            "judge_decision": "Moderate risk strategy recommended..."
        }
    }

@pytest.fixture
def mock_welcome_file(tmp_path):
    """Create a temporary welcome.txt file."""
    welcome_file = tmp_path / "welcome.txt"
    welcome_file.write_text("Welcome to TradingAgents!")
    return welcome_file

@pytest.fixture
def mock_layout():
    """Provide a mocked rich layout instance."""
    layout = MagicMock()
    # Mock the dictionary-like access to layout sections
    layout.__getitem__ = lambda self, key: MagicMock()
    return layout

@pytest.fixture
def mock_message_buffer():
    """Provide a mocked message buffer with predefined states."""
    buffer = Mock()
    buffer.messages = []
    buffer.tool_calls = []
    buffer.current_report = None
    buffer.agent_status = {
        "Market Analyst": "pending",
        "Social Analyst": "pending",
        "News Analyst": "pending",
        "Fundamentals Analyst": "pending",
        "Bull Researcher": "pending",
        "Bear Researcher": "pending",
        "Research Manager": "pending",
        "Trader": "pending",
        "Risky Analyst": "pending",
        "Neutral Analyst": "pending",
        "Safe Analyst": "pending",
        "Portfolio Manager": "pending"
    }
    return buffer

@pytest.fixture
def mock_config():
    """Provide mocked configuration settings."""
    return {
        "max_debate_rounds": 3,
        "max_risk_discuss_rounds": 3,
        "quick_think_llm": "DeepSeek V3",
        "deep_think_llm": "DeepSeek V3"
    }

@pytest.fixture
def sample_report_sections():
    """Provide sample report section titles and content."""
    return {
        "市场分析": "market_report",
        "社会情绪": "sentiment_report",
        "新闻分析": "news_report",
        "基本面分析": "fundamentals_report",
        "研究团队决策": "investment_plan",
        "交易团队计划": "trader_investment_plan",
        "投资组合管理决策": "final_trade_decision"
    }

@pytest.fixture
def mock_panel():
    """Provide a mocked rich panel instance."""
    return Mock()

@pytest.fixture
def mock_markdown():
    """Provide a mocked rich markdown instance."""
    return Mock()

@pytest.fixture
def mock_spinner():
    """Provide a mocked rich spinner instance."""
    return Mock()