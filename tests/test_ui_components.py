import pytest
from unittest.mock import patch
from cli.main import (
    create_question_box,
    create_layout,
    update_display,
    extract_content_string,
)

class TestUIComponents:
    def test_create_question_box(self, mock_panel):
        """Test question box creation with various inputs."""
        # Test with all parameters
        box = create_question_box("Test Title", "Test Prompt", "Default")
        assert "Test Title" in str(box)
        assert "Test Prompt" in str(box)
        assert "Default" in str(box)

        # Test without default value
        box = create_question_box("Test Title", "Test Prompt")
        assert "Test Title" in str(box)
        assert "Test Prompt" in str(box)

    def test_layout_structure(self):
        """Test layout creation and structure."""
        layout = create_layout()
        
        # Verify main sections exist
        assert "header" in layout
        assert "main" in layout
        assert "footer" in layout
        
        # Verify sub-sections
        assert "upper" in layout["main"]
        assert "analysis" in layout["main"]
        assert "progress" in layout["upper"]
        assert "messages" in layout["upper"]

    @patch('cli.main.Panel')
    @patch('cli.main.Markdown')
    def test_display_update(self, mock_markdown, mock_panel, mock_layout, mock_message_buffer):
        """Test display update functionality."""
        # Set up message buffer with some test data
        mock_message_buffer.tool_calls = [
            ("12:00:00", "test_tool", "test args")
        ]
        mock_message_buffer.messages = [
            ("12:00:01", "info", "test message")
        ]
        mock_message_buffer.current_report = "# Test Report\nReport content"

        # Test display update with spinner
        update_display(mock_layout, "Processing...")
        
        # Verify header update was called
        mock_layout["header"].update.assert_called()
        
        # Verify progress table update
        mock_layout["progress"].update.assert_called()
        
        # Verify messages table update
        mock_layout["messages"].update.assert_called()
        
        # Verify analysis panel update
        mock_layout["analysis"].update.assert_called()
        
        # Verify footer update
        mock_layout["footer"].update.assert_called()

    def test_content_string_extraction(self):
        """Test extraction of content strings from various formats."""
        # Test string input
        assert extract_content_string("test string") == "test string"
        
        # Test list of strings
        assert extract_content_string(["test1", "test2"]) == "test1 test2"
        
        # Test Anthropic format
        content = [
            {"type": "text", "text": "message"},
            {"type": "tool_use", "name": "tool"}
        ]
        result = extract_content_string(content)
        assert "message" in result
        assert "tool" in result

        # Test mixed content
        mixed = [
            "plain text",
            {"type": "text", "text": "structured"},
            123
        ]
        result = extract_content_string(mixed)
        assert "plain text" in result
        assert "structured" in result
        assert "123" in result

@pytest.mark.integration
class TestUIIntegration:
    @patch('cli.main.console')
    def test_display_workflow(self, mock_console, mock_message_buffer, sample_state_data):
        """Test the complete display workflow."""
        layout = create_layout()
        
        # Initial display
        update_display(layout)
        mock_console.print.assert_called()
        
        # Update with analysis data
        mock_message_buffer.current_report = "# New Analysis\nTest content"
        update_display(layout)
        mock_console.print.assert_called()
        
        # Update with spinner
        update_display(layout, "Processing request...")
        mock_console.print.assert_called()

    @patch('cli.main.typer.prompt')
    @patch('cli.main.console')
    def test_user_interaction_workflow(self, mock_console, mock_prompt, 
                                    mock_welcome_file, sample_selections):
        """Test the user interaction workflow."""
        from cli.main import get_user_selections
        
        # Mock user inputs
        mock_prompt.side_effect = [
            sample_selections["ticker"],
            sample_selections["analysis_date"]
        ]
        
        # Test the selection process
        with patch('cli.main.select_analysts') as mock_analysts:
            mock_analysts.return_value = sample_selections["analysts"]
            
            with patch('cli.main.select_research_depth') as mock_depth:
                mock_depth.return_value = sample_selections["research_depth"]
                
                with patch('cli.main.select_llm_provider') as mock_llm:
                    mock_llm.return_value = (
                        sample_selections["llm_provider"],
                        sample_selections["backend_url"]
                    )
                    
                    result = get_user_selections()
                    
                    assert result["ticker"] == sample_selections["ticker"]
                    assert result["analysis_date"] == sample_selections["analysis_date"]
                    assert result["analysts"] == sample_selections["analysts"]
                    assert result["research_depth"] == sample_selections["research_depth"]
                    assert result["llm_provider"] == sample_selections["llm_provider"].lower()
                    assert result["backend_url"] == sample_selections["backend_url"]

if __name__ == '__main__':
    pytest.main([__file__])