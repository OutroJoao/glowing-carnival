"""MCP server for Gmail operations."""

import json
from typing import Any

from src.tools.gmail_tools import GmailClient
from src.config.settings import Settings


class GmailMCPServer:
    """MCP server wrapper for Gmail operations."""

    def __init__(self, settings: Settings):
        """Initialize Gmail MCP server."""
        self.client = GmailClient(settings)
        self.tools = self._create_tools()

    def _create_tools(self) -> list[dict[str, Any]]:
        """Create tool definitions for MCP."""
        return [
            {
                "name": "send_email",
                "description": "Send an email to a recipient",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "to": {
                            "type": "string",
                            "description": "Recipient email address",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Email subject",
                        },
                        "body": {
                            "type": "string",
                            "description": "Email body text or HTML",
                        },
                        "html": {
                            "type": "boolean",
                            "description": "Whether body is HTML (default: false)",
                            "default": False,
                        },
                        "cc": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of CC recipients",
                        },
                        "bcc": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of BCC recipients",
                        },
                    },
                    "required": ["to", "subject", "body"],
                },
            },
            {
                "name": "read_emails",
                "description": "Read emails from inbox matching a query",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": 'Gmail search query (default: "is:unread")',
                            "default": "is:unread",
                        },
                        "max_results": {
                            "type": "integer",
                            "description": "Maximum number of emails to retrieve (default: 10)",
                            "default": 10,
                        },
                    },
                },
            },
            {
                "name": "reply_to_email",
                "description": "Reply to an email in a thread",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "thread_id": {
                            "type": "string",
                            "description": "Gmail thread ID",
                        },
                        "subject": {
                            "type": "string",
                            "description": "Reply subject",
                        },
                        "body": {
                            "type": "string",
                            "description": "Reply body",
                        },
                        "html": {
                            "type": "boolean",
                            "description": "Whether body is HTML (default: false)",
                            "default": False,
                        },
                    },
                    "required": ["thread_id", "subject", "body"],
                },
            },
            {
                "name": "mark_as_read",
                "description": "Mark an email as read",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "message_id": {
                            "type": "string",
                            "description": "Gmail message ID",
                        },
                    },
                    "required": ["message_id"],
                },
            },
        ]

    def execute_tool(self, tool_name: str, tool_input: dict[str, Any]) -> str:
        """Execute a tool and return the result."""
        try:
            if tool_name == "send_email":
                message_id = self.client.send_email(**tool_input)
                return json.dumps({"success": True, "message_id": message_id})

            elif tool_name == "read_emails":
                emails = self.client.read_emails(**tool_input)
                return json.dumps({"success": True, "emails": emails})

            elif tool_name == "reply_to_email":
                message_id = self.client.reply_to_email(**tool_input)
                return json.dumps({"success": True, "message_id": message_id})

            elif tool_name == "mark_as_read":
                self.client.mark_as_read(tool_input["message_id"])
                return json.dumps({"success": True})

            else:
                return json.dumps({"success": False, "error": f"Unknown tool: {tool_name}"})

        except Exception as e:
            return json.dumps({"success": False, "error": str(e)})

    def get_tools(self) -> list[dict[str, Any]]:
        """Return the list of available tools."""
        return self.tools
