"""Tests for MCP servers."""

import json
from unittest.mock import MagicMock, patch
import pytest

from src.mcp_servers.gmail_server import GmailMCPServer
from src.mcp_servers.sheets_server import SheetsMCPServer


class TestGmailMCPServer:
    """Test Gmail MCP Server."""

    @patch("src.mcp_servers.gmail_server.GmailClient")
    def test_gmail_server_initialization(self, mock_client, test_settings):
        """Test initializing Gmail MCP server."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = GmailMCPServer(test_settings)

        assert server.tools is not None
        assert len(server.tools) > 0

    @patch("src.mcp_servers.gmail_server.GmailClient")
    def test_gmail_server_tools(self, mock_client, test_settings):
        """Test Gmail server has correct tools."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = GmailMCPServer(test_settings)
        tool_names = {tool["name"] for tool in server.tools}

        assert "send_email" in tool_names
        assert "read_emails" in tool_names
        assert "reply_to_email" in tool_names
        assert "mark_as_read" in tool_names

    @patch("src.mcp_servers.gmail_server.GmailClient")
    def test_gmail_server_send_email(self, mock_client, test_settings):
        """Test executing send_email tool."""
        mock_client_instance = MagicMock()
        mock_client_instance.send_email.return_value = "msg-123"
        mock_client.return_value = mock_client_instance

        server = GmailMCPServer(test_settings)
        result = server.execute_tool(
            "send_email",
            {"to": "test@example.com", "subject": "Test", "body": "Test body"}
        )

        result_data = json.loads(result)
        assert result_data["success"] is True
        assert result_data["message_id"] == "msg-123"

    @patch("src.mcp_servers.gmail_server.GmailClient")
    def test_gmail_server_read_emails(self, mock_client, test_settings):
        """Test executing read_emails tool."""
        mock_client_instance = MagicMock()
        mock_client_instance.read_emails.return_value = [
            {
                "id": "msg-1",
                "subject": "Test",
                "from": "sender@example.com",
            }
        ]
        mock_client.return_value = mock_client_instance

        server = GmailMCPServer(test_settings)
        result = server.execute_tool(
            "read_emails",
            {"query": "is:unread", "max_results": 10}
        )

        result_data = json.loads(result)
        assert result_data["success"] is True
        assert len(result_data["emails"]) > 0

    @patch("src.mcp_servers.gmail_server.GmailClient")
    def test_gmail_server_unknown_tool(self, mock_client, test_settings):
        """Test executing unknown tool."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = GmailMCPServer(test_settings)
        result = server.execute_tool("unknown_tool", {})

        result_data = json.loads(result)
        assert result_data["success"] is False


class TestSheetsMCPServer:
    """Test Google Sheets MCP Server."""

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_initialization(self, mock_client, test_settings):
        """Test initializing Sheets MCP server."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)

        assert server.tools is not None
        assert len(server.tools) > 0

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_tools(self, mock_client, test_settings):
        """Test Sheets server has correct tools."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)
        tool_names = {tool["name"] for tool in server.tools}

        assert "read_sheet" in tool_names
        assert "write_sheet" in tool_names
        assert "append_row" in tool_names
        assert "get_residents" in tool_names
        assert "get_overdue_quotas" in tool_names
        assert "log_incident" in tool_names
        assert "get_incidents" in tool_names

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_read_sheet(self, mock_client, test_settings):
        """Test executing read_sheet tool."""
        mock_client_instance = MagicMock()
        mock_client_instance.read_sheet.return_value = [
            ["Nome", "Apartamento"],
            ["João", "101"],
        ]
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)
        result = server.execute_tool(
            "read_sheet",
            {
                "spreadsheet_id": "test-id",
                "sheet_name": "Residents",
            }
        )

        result_data = json.loads(result)
        assert result_data["success"] is True
        assert len(result_data["data"]) > 0

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_get_residents(self, mock_client, test_settings):
        """Test executing get_residents tool."""
        mock_client_instance = MagicMock()
        mock_client_instance.get_residents.return_value = [
            {"Nome": "João Silva", "Apartamento": "101"},
            {"Nome": "Maria Santos", "Apartamento": "102"},
        ]
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)
        result = server.execute_tool("get_residents", {})

        result_data = json.loads(result)
        assert result_data["success"] is True
        assert len(result_data["residents"]) == 2

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_log_incident(self, mock_client, test_settings):
        """Test executing log_incident tool."""
        mock_client_instance = MagicMock()
        mock_client_instance.log_incident.return_value = "Incidents!A2"
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)
        result = server.execute_tool(
            "log_incident",
            {
                "resident": "João Silva",
                "description": "Teste",
                "priority": "Normal",
                "status": "Aberta",
            }
        )

        result_data = json.loads(result)
        assert result_data["success"] is True

    @patch("src.mcp_servers.sheets_server.SheetsClient")
    def test_sheets_server_unknown_tool(self, mock_client, test_settings):
        """Test executing unknown tool."""
        mock_client_instance = MagicMock()
        mock_client.return_value = mock_client_instance

        server = SheetsMCPServer(test_settings)
        result = server.execute_tool("unknown_tool", {})

        result_data = json.loads(result)
        assert result_data["success"] is False
