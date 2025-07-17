import pytest
import datetime
from unittest.mock import Mock, patch, MagicMock
from unittest.mock import mock_open
from cli.main import (
    MessageBuffer,
    get_ticker,
    get_analysis_date,
    create_layout,
    update_display,
    get_user_selections,
    display_complete_report,
    update_research_team_status,
    extract_content_string,
    run_analysis,
)
from cli.models import AnalystType

@pytest.fixture
def message_buffer():
    return MessageBuffer()

@pytest.fixture
def mock_console():
    return Mock()

@pytest.fixture
def sample_report_data():
    return {
        "market_report": "Market analysis content",
        "sentiment_report": "Sentiment analysis content",
        "news_report": "News analysis content",
        "fundamentals_report": "Fundamentals analysis content",
        "investment_debate_state": {
            "bull_history": "Bull analysis",
            "bear_history": "Bear analysis",
            "judge_decision": "Research manager decision"
        },
        "trader_investment_plan": "Trading plan content",
        "risk_debate_state": {
            "risky_history": "Risky analysis",
            "safe_history": "Safe analysis",
            "neutral_history": "Neutral analysis",
            "judge_decision": "Risk manager decision"
        }
    }

class TestMessageBuffer:
    def test_init(self, message_buffer):
        assert message_buffer.messages.maxlen == 100
        assert message_buffer.tool_calls.maxlen == 100
        assert message_buffer.current_report is None
        assert message_buffer.final_report is None
        assert len(message_buffer.agent_status) > 0
        assert message_buffer.current_agent is None

    def test_add_message(self, message_buffer):
        message_buffer.add_message("test_type", "test_content")
        assert len(message_buffer.messages) == 1
        _, msg_type, content = message_buffer.messages[0]
        assert msg_type == "test_type"
        assert content == "test_content"

    def test_add_tool_call(self, message_buffer):
        message_buffer.add_tool_call("test_tool", {"arg": "value"})
        assert len(message_buffer.tool_calls) == 1
        _, tool_name, args = message_buffer.tool_calls[0]
        assert tool_name == "test_tool"
        assert args == {"arg": "value"}

    def test_update_agent_status(self, message_buffer):
        agent = "Market Analyst"
        message_buffer.update_agent_status(agent, "in_progress")
        assert message_buffer.agent_status[agent] == "in_progress"
        assert message_buffer.current_agent == agent

    def test_update_report_section(self, message_buffer):
        section = "market_report"
        content = "Test market analysis"
        message_buffer.update_report_section(section, content)
        assert message_buffer.report_sections[section] == content
        assert "市场分析" in message_buffer.current_report

@patch('cli.main.typer.prompt')
def test_get_ticker(mock_prompt):
    mock_prompt.return_value = "603127.SH"
    result = get_ticker()
    assert result == "603127.SH"
    mock_prompt.assert_called_once_with("", default="SPY")

@patch('cli.main.typer.prompt')
def test_get_analysis_date(mock_prompt):
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    mock_prompt.return_value = today
    result = get_analysis_date()
    assert result == today
    mock_prompt.assert_called_once()

def test_create_layout():
    layout = create_layout()
    assert layout["header"] is not None
    assert layout["main"] is not None
    assert layout["footer"] is not None
    assert layout["upper"] is not None
    assert layout["analysis"] is not None
    assert layout["progress"] is not None
    assert layout["messages"] is not None

@patch('cli.main.Panel')
@patch('cli.main.console')
def test_display_complete_report(mock_console, mock_panel, sample_report_data):
    display_complete_report(sample_report_data)
    assert mock_console.print.call_count > 0
    assert mock_panel.call_count > 0

@patch('cli.main.message_buffer', new_callable=MagicMock)
def test_update_research_team_status(mock_message_buffer):
    update_research_team_status("completed")
    # Assert that update_agent_status was called with 'completed' for each research team member
    research_team = ["Bull Researcher", "Bear Researcher", "Research Manager", "Trader"]
    for agent in research_team:
        mock_message_buffer.update_agent_status.assert_any_call(agent, "completed")

def test_extract_content_string():
    # Test string input
    assert extract_content_string("test") == "test"

    # Test list input with dict items
    content_list = [
        {"type": "text", "text": "hello"},
        {"type": "tool_use", "name": "test_tool"}
    ]
    result = extract_content_string(content_list)
    assert "hello" in result
    assert "test_tool" in result

@patch('cli.main.console')
@patch('cli.main.select_analysts')
@patch('cli.main.select_research_depth')
@patch('cli.main.select_llm_provider')
@patch('cli.main.select_shallow_thinking_agent')
@patch('cli.main.select_deep_thinking_agent')
def test_get_user_selections(
    mock_deep_agent,
    mock_shallow_agent,
    mock_llm,
    mock_depth,
    mock_analysts,
    mock_console
):
    mock_analysts.return_value = [AnalystType.MARKET, AnalystType.NEWS]
    mock_depth.return_value = "shallow"
    mock_llm.return_value = ("openrouter", "https://api.example.com")
    mock_shallow_agent.return_value = "model1"
    mock_deep_agent.return_value = "model2"

    with patch('cli.main.get_ticker') as mock_ticker:
        with patch('cli.main.get_analysis_date') as mock_date:
            mock_ticker.return_value = "603127.SH"
            mock_date.return_value = "2025-07-08"
            
            result = get_user_selections()
            
            assert result["ticker"] == "603127.SH"
            assert result["analysis_date"] == "2025-07-08"
            assert result["analysts"] == [AnalystType.MARKET, AnalystType.NEWS]
            assert result["research_depth"] == "shallow"
            assert result["llm_provider"] == "openrouter"
            assert result["backend_url"] == "https://api.example.com"
            assert result["shallow_thinker"] == "model1"
            assert result["deep_thinker"] == "model2"

def test_update_display(message_buffer):
    layout = create_layout()
    update_display(layout, "Testing display update")
    
    # Verify header update
    assert layout["header"].renderable is not None
    
    # Verify main content sections
    assert layout["progress"].renderable is not None
    assert layout["messages"].renderable is not None
    assert layout["analysis"].renderable is not None
    
    # Verify footer update
    assert layout["footer"].renderable is not None



@patch('cli.main.get_user_selections')
@patch('cli.main.TradingAgentsGraph')
@patch('cli.main.Live')
@patch('cli.main.display_complete_report')
@patch('pathlib.Path.mkdir')
@patch('pathlib.Path.touch')
@patch('builtins.open', new_callable=mock_open)
def test_run_analysis(
    mock_open_file,
    mock_touch,
    mock_mkdir,
    mock_display_report,
    mock_live,
    mock_trading_agents_graph,
    mock_get_user_selections,
):
    """Test the main analysis workflow orchestrator."""
    # 1. Setup Mocks
    mock_selections = {
        "ticker": "603127.SH",
        "analysis_date": "2025-07-09",
        "analysts": [AnalystType.MARKET, AnalystType.NEWS],
        "research_depth": 2,
        "llm_provider": "openrouter",
        "backend_url": "https://api.example.com",
        "shallow_thinker": "model1",
        "deep_thinker": "model2",
    }
    mock_get_user_selections.return_value = mock_selections

    mock_graph_instance = MagicMock()
    mock_final_state = {"final_report": "some analysis"}

    # Simulate the generator behavior by returning a generator that yields the final state
    def propagate_generator(*args, **kwargs):
        yield mock_final_state

    mock_graph_instance.propagate.side_effect = propagate_generator
    mock_trading_agents_graph.return_value = mock_graph_instance

    # Configure the Live mock to act as a context manager
    live_instance = MagicMock()
    mock_live.return_value = live_instance
    live_instance.__enter__.return_value = None  # Simulate entering the context

    # 2. Run the function
    run_analysis()

    # 3. Assertions
    mock_get_user_selections.assert_called_once()

    # Assert TradingAgentsGraph was initialized correctly
    mock_trading_agents_graph.assert_called_once()
    _, kwargs = mock_trading_agents_graph.call_args
    assert kwargs['config']['max_debate_rounds'] == 2
    assert kwargs['config']['quick_think_llm'] == "model1"
    assert kwargs['config']['deep_think_llm'] == "model2"
    assert kwargs['config']['llm_provider'] == "openrouter"

    # Assert propagate was called correctly
    mock_graph_instance.propagate.assert_called_once_with(
        mock_selections["ticker"], mock_selections["analysis_date"]
    )

    # Assert UI/File operations were called
    mock_live.assert_called_once()
    mock_display_report.assert_called_once_with(mock_final_state)
    assert mock_mkdir.called
    assert mock_open_file.called


if __name__ == '__main__':
    pytest.main([__file__])