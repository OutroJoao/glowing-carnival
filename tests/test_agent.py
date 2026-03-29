"""Tests for the main agent."""

import json
from unittest.mock import MagicMock, patch, Mock
import pytest

from src.agent.main import CondominiumAgent


class TestCondominiumAgent:
    """Test CondominiumAgent class."""

    @patch("src.agent.main.Anthropic")
    @patch("src.agent.main.GmailMCPServer")
    @patch("src.agent.main.SheetsMCPServer")
    def test_agent_initialization(self, mock_sheets, mock_gmail, mock_anthropic, test_settings):
        """Test agent initialization."""
        # Setup mocks
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance
        mock_gmail_instance.get_tools.return_value = [
            {
                "name": "send_email",
                "description": "Send an email",
                "inputSchema": {"type": "object"},
            }
        ]

        mock_sheets_instance = MagicMock()
        mock_sheets.return_value = mock_sheets_instance
        mock_sheets_instance.get_tools.return_value = [
            {
                "name": "read_sheet",
                "description": "Read sheet",
                "inputSchema": {"type": "object"},
            }
        ]

        mock_anthropic_instance = MagicMock()
        mock_anthropic.return_value = mock_anthropic_instance

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            agent = CondominiumAgent()

            assert agent.client is not None
            assert agent.gmail_server is not None
            assert agent.sheets_server is not None
            assert agent.all_tools is not None

    @patch("src.agent.main.Anthropic")
    @patch("src.agent.main.GmailMCPServer")
    @patch("src.agent.main.SheetsMCPServer")
    def test_agent_tools_conversion(self, mock_sheets, mock_gmail, mock_anthropic, test_settings):
        """Test that tools are properly converted for API."""
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance
        mock_gmail_instance.get_tools.return_value = [
            {
                "name": "send_email",
                "description": "Send email",
                "inputSchema": {"type": "object", "properties": {}},
            }
        ]

        mock_sheets_instance = MagicMock()
        mock_sheets.return_value = mock_sheets_instance
        mock_sheets_instance.get_tools.return_value = []

        mock_anthropic_instance = MagicMock()
        mock_anthropic.return_value = mock_anthropic_instance

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            agent = CondominiumAgent()

            # Check tools are properly formatted for API
            assert len(agent.all_tools) > 0
            assert all(tool["type"] == "function" for tool in agent.all_tools)
            assert all("function" in tool for tool in agent.all_tools)

    @patch("src.agent.main.Anthropic")
    @patch("src.agent.main.GmailMCPServer")
    @patch("src.agent.main.SheetsMCPServer")
    def test_agent_process_tool_call_gmail(self, mock_sheets, mock_gmail, mock_anthropic, test_settings):
        """Test processing a Gmail tool call."""
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance
        mock_gmail_instance.get_tools.return_value = [
            {"name": "send_email", "description": "Send", "inputSchema": {}}
        ]
        mock_gmail_instance.execute_tool.return_value = '{"success": true}'

        mock_sheets_instance = MagicMock()
        mock_sheets.return_value = mock_sheets_instance
        mock_sheets_instance.get_tools.return_value = []

        mock_anthropic_instance = MagicMock()
        mock_anthropic.return_value = mock_anthropic_instance

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            agent = CondominiumAgent()

            result = agent.process_tool_call(
                "send_email",
                {"to": "test@example.com", "subject": "Test", "body": "Test"}
            )

            assert result is not None
            mock_gmail_instance.execute_tool.assert_called_once()

    @patch("src.agent.main.Anthropic")
    @patch("src.agent.main.GmailMCPServer")
    @patch("src.agent.main.SheetsMCPServer")
    def test_agent_process_tool_call_sheets(self, mock_sheets, mock_gmail, mock_anthropic, test_settings):
        """Test processing a Sheets tool call."""
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance
        mock_gmail_instance.get_tools.return_value = []

        mock_sheets_instance = MagicMock()
        mock_sheets.return_value = mock_sheets_instance
        mock_sheets_instance.get_tools.return_value = [
            {"name": "read_sheet", "description": "Read", "inputSchema": {}}
        ]
        mock_sheets_instance.execute_tool.return_value = '{"success": true}'

        mock_anthropic_instance = MagicMock()
        mock_anthropic.return_value = mock_anthropic_instance

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            agent = CondominiumAgent()

            result = agent.process_tool_call(
                "read_sheet",
                {"spreadsheet_id": "test", "sheet_name": "Test"}
            )

            assert result is not None
            mock_sheets_instance.execute_tool.assert_called_once()

    @patch("src.agent.main.Anthropic")
    @patch("src.agent.main.GmailMCPServer")
    @patch("src.agent.main.SheetsMCPServer")
    def test_agent_process_unknown_tool(self, mock_sheets, mock_gmail, mock_anthropic, test_settings):
        """Test processing an unknown tool."""
        mock_gmail_instance = MagicMock()
        mock_gmail.return_value = mock_gmail_instance
        mock_gmail_instance.get_tools.return_value = []

        mock_sheets_instance = MagicMock()
        mock_sheets.return_value = mock_sheets_instance
        mock_sheets_instance.get_tools.return_value = []

        mock_anthropic_instance = MagicMock()
        mock_anthropic.return_value = mock_anthropic_instance

        with patch.dict("os.environ", {"ANTHROPIC_API_KEY": "test-key"}):
            agent = CondominiumAgent()

            result = agent.process_tool_call("unknown_tool", {})

            assert "error" in result or "Unknown" in result
