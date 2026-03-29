"""MCP server for Google Sheets operations."""

import json
from typing import Any

from src.tools.sheets_tools import SheetsClient
from src.config.settings import Settings


class SheetsMCPServer:
    """MCP server wrapper for Google Sheets operations."""

    def __init__(self, settings: Settings):
        """Initialize Sheets MCP server."""
        self.client = SheetsClient(settings)
        self.tools = self._create_tools()

    def _create_tools(self) -> list[dict[str, Any]]:
        """Create tool definitions for MCP."""
        return [
            {
                "name": "read_sheet",
                "description": "Read data from a Google Sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "type": "string",
                            "description": "Google Sheets ID",
                        },
                        "sheet_name": {
                            "type": "string",
                            "description": "Sheet name",
                        },
                        "range_notation": {
                            "type": "string",
                            "description": "Optional range (e.g., 'A1:D10')",
                        },
                    },
                    "required": ["spreadsheet_id", "sheet_name"],
                },
            },
            {
                "name": "write_sheet",
                "description": "Write data to a Google Sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "type": "string",
                            "description": "Google Sheets ID",
                        },
                        "sheet_name": {
                            "type": "string",
                            "description": "Sheet name",
                        },
                        "range_notation": {
                            "type": "string",
                            "description": "Range to write to (e.g., 'A1')",
                        },
                        "values": {
                            "type": "array",
                            "description": "List of rows to write",
                            "items": {"type": "array"},
                        },
                    },
                    "required": ["spreadsheet_id", "sheet_name", "range_notation", "values"],
                },
            },
            {
                "name": "append_row",
                "description": "Append a row to a Google Sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "spreadsheet_id": {
                            "type": "string",
                            "description": "Google Sheets ID",
                        },
                        "sheet_name": {
                            "type": "string",
                            "description": "Sheet name",
                        },
                        "row": {
                            "type": "array",
                            "description": "Row data to append",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["spreadsheet_id", "sheet_name", "row"],
                },
            },
            {
                "name": "get_residents",
                "description": "Get all residents from the residents sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "get_overdue_quotas",
                "description": "Get all overdue quotas from the quotas sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {},
                },
            },
            {
                "name": "log_incident",
                "description": "Log a new incident in the incidents sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "resident": {
                            "type": "string",
                            "description": "Resident name or apartment",
                        },
                        "description": {
                            "type": "string",
                            "description": "Incident description",
                        },
                        "priority": {
                            "type": "string",
                            "description": "Priority level (Baixa, Normal, Alta)",
                            "default": "Normal",
                        },
                        "status": {
                            "type": "string",
                            "description": "Current status (Aberta, Em Progresso, Fechada)",
                            "default": "Aberta",
                        },
                    },
                    "required": ["resident", "description"],
                },
            },
            {
                "name": "get_incidents",
                "description": "Get incidents from the incidents sheet",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "description": "Filter by status (e.g., 'Aberta', 'Fechada')",
                        },
                    },
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        """Execute a tool and return the result."""
        try:
            if tool_name == "read_sheet":
                data = self.client.read_sheet(**tool_input)
                return json.dumps({"success": True, "data": data})

            elif tool_name == "write_sheet":
                updated_cells = self.client.write_sheet(**tool_input)
                return json.dumps({"success": True, "updated_cells": updated_cells})

            elif tool_name == "append_row":
                updated_range = self.client.append_row(**tool_input)
                return json.dumps({"success": True, "updated_range": updated_range})

            elif tool_name == "get_residents":
                residents = self.client.get_residents()
                return json.dumps({"success": True, "residents": residents})

            elif tool_name == "get_overdue_quotas":
                overdue = self.client.get_overdue_quotas()
                return json.dumps({"success": True, "overdue_quotas": overdue})

            elif tool_name == "log_incident":
                updated_range = self.client.log_incident(**tool_input)
                return json.dumps({"success": True, "updated_range": updated_range})

            elif tool_name == "get_incidents":
                incidents = self.client.get_incidents(**tool_input)
                return json.dumps({"success": True, "incidents": incidents})

            else:
                return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    def get_tools(self) -> list[dict[str, Any]]:
        """Return the list of available tools."""
        return self.tools
