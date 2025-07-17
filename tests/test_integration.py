import pytest
import datetime
from unittest.mock import patch, Mock
from cli.main import (
    get_user_selections,
    run_analysis,
    TradingAgentsGraph,
    DEFAULT_CONFIG
)

class TestDataFlow:
    @pytest.fixture
    def setup_trading_graph(self, mock_config):
        """Set up a trading graph instance with mocked configuration."""
        return TradingAgentsGraph(mock_config)

    def test_message_flow(self, mock_message_buffer):
        """Test message flow through the system."""
        # Add various types of messages
        mock_message_buffer.add_message("info", "Test info message")
        mock_message_buffer.add_message("error", "Test error message")
        mock_message_buffer.add_tool_call("data_fetch", {"symbol": "603127.SH"})
        
        # Verify message handling
        assert len(mock_message_buffer.messages) == 2
        assert len(mock_message_buffer.tool_calls) == 1
        
        # Verify message order
        assert mock_message_buffer.messages[0][1] == "info"
        assert mock_message_buffer.messages[1][1] == "error"

    def test_report_flow(self, mock_message_buffer, sample_state_data):
        """Test report generation and update flow."""
        # Update various report sections
        mock_message_buffer.update_report_section("market_report", sample_state_data["market_report"])
        mock_message_buffer.update_report_section("sentiment_report", sample_state_data["sentiment_report"])
        
        # Verify report updates
        assert mock_message_buffer.report_sections["market_report"] == sample_state_data["market_report"]
        assert mock_message_buffer.report_sections["sentiment_report"] == sample_state_data["sentiment_report"]
        
        # Verify current report contains latest update
        assert mock_message_buffer.current_report is not None
        assert "市场分析" in mock_message_buffer.current_report or "社会情绪" in mock_message_buffer.current_report

@pytest.mark.integration
class TestSystemIntegration:
    @patch('cli.main.TradingAgentsGraph')
    def test_complete_analysis_flow(self, mock_trading_graph, sample_selections, 
                                  mock_message_buffer, sample_state_data):
        """Test complete analysis workflow."""
        # Mock trading graph execution
        mock_graph_instance = Mock()
        mock_trading_graph.return_value = mock_graph_instance
        mock_graph_instance.run.return_value = sample_state_data

        with patch('cli.main.get_user_selections') as mock_selections:
            mock_selections.return_value = sample_selections
            
            # Run analysis
            try:
                run_analysis()
                
                # Verify trading graph initialization
                mock_trading_graph.assert_called_once()
                
                # Verify graph execution
                mock_graph_instance.run.assert_called_once()
                
                # Verify results processing
                assert mock_message_buffer.final_report is not None
                
            except Exception as e:
                pytest.fail(f"Analysis flow failed: {str(e)}")

    def test_agent_status_updates(self, mock_message_buffer):
        """Test agent status updates during analysis."""
        agents = [
            "Market Analyst",
            "Social Analyst",
            "News Analyst",
            "Fundamentals Analyst",
            "Bull Researcher",
            "Bear Researcher",
            "Research Manager",
            "Trader"
        ]
        
        # Simulate agent status transitions
        for agent in agents:
            mock_message_buffer.update_agent_status(agent, "in_progress")
            assert mock_message_buffer.agent_status[agent] == "in_progress"
            
            mock_message_buffer.update_agent_status(agent, "completed")
            assert mock_message_buffer.agent_status[agent] == "completed"

    @patch('cli.main.typer.prompt')
    @patch('cli.main.console')
    def test_user_input_validation(self, mock_console, mock_prompt):
        """Test user input validation and error handling."""
        # Test stock code validation
        mock_prompt.return_value = "INVALID"
        with pytest.raises(ValueError):
            get_user_selections()
        
        # Test date validation
        mock_prompt.return_value = "2025-13-45"  # Invalid date
        with pytest.raises(ValueError):
            get_user_selections()
        
        # Test future date rejection
        future_date = (datetime.datetime.now() + datetime.timedelta(days=365)).strftime("%Y-%m-%d")
        mock_prompt.return_value = future_date
        with pytest.raises(ValueError):
            get_user_selections()

@pytest.mark.config
class TestConfiguration:
    def test_config_validation(self, mock_config):
        """Test configuration validation."""
        # Test required fields
        required_fields = [
            "max_debate_rounds",
            "max_risk_discuss_rounds",
            "quick_think_llm",
            "deep_think_llm"
        ]
        for field in required_fields:
            assert field in mock_config
        
        # Test value ranges
        assert 1 <= mock_config["max_debate_rounds"] <= 10
        assert 1 <= mock_config["max_risk_discuss_rounds"] <= 10
        
        # Test model names
        assert isinstance(mock_config["quick_think_llm"], str)
        assert isinstance(mock_config["deep_think_llm"], str)

    def test_config_override(self):
        """Test configuration override behavior."""
        base_config = DEFAULT_CONFIG.copy()
        custom_config = {
            "max_debate_rounds": 5,
            "quick_think_llm": "Custom Model"
        }
        
        # Override base config
        config = {**base_config, **custom_config}
        
        # Verify overrides
        assert config["max_debate_rounds"] == 5
        assert config["quick_think_llm"] == "Custom Model"
        
        # Verify unchanged values
        assert config["max_risk_discuss_rounds"] == base_config["max_risk_discuss_rounds"]

if __name__ == '__main__':
    pytest.main([__file__])