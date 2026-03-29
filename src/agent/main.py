"""Main agent entry point."""

import logging
import os
from typing import Optional

from anthropic import Anthropic

from src.config.settings import Settings
from src.agent.system_prompt import get_system_prompt
from src.mcp_servers.gmail_server import GmailMCPServer
from src.mcp_servers.sheets_server import SheetsMCPServer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class CondominiumAgent:
    """Autonomous condominium management agent."""

    def __init__(self):
        """Initialize the agent."""
        # Load settings from environment
        self.settings = Settings()

        # Initialize clients
        self.gmail_server = GmailMCPServer(self.settings)
        self.sheets_server = SheetsMCPServer(self.settings)

        # Initialize Anthropic client
        self.client = Anthropic(api_key=self.settings.anthropic_api_key)

        # Get system prompt
        self.system_prompt = get_system_prompt(self.settings.agent_language)

        # Combine all available tools
        self.all_tools = (
            self._convert_tools_for_api(self.gmail_server.get_tools())
            + self._convert_tools_for_api(self.sheets_server.get_tools())
        )

        logger.info(f"Agent '{self.settings.agent_name}' initialized successfully")

    def _convert_tools_for_api(self, tools: list) -> list:
        """Convert tools to Anthropic API format."""
        return [
            {
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["inputSchema"],
                },
            }
            for tool in tools
        ]

    def process_tool_call(
        self, tool_name: str, tool_input: dict
    ) -> Optional[str]:
        """Process a tool call and return the result."""
        logger.info(f"Processing tool call: {tool_name}")

        # Determine which server the tool belongs to
        gmail_tools = {t["name"] for t in self.gmail_server.get_tools()}
        sheets_tools = {t["name"] for t in self.sheets_server.get_tools()}

        if tool_name in gmail_tools:
            return self.gmail_server.execute_tool(tool_name, tool_input)
        elif tool_name in sheets_tools:
            return self.sheets_server.execute_tool(tool_name, tool_input)
        else:
            logger.error(f"Unknown tool: {tool_name}")
            return '{"success": false, "error": "Unknown tool"}'

    def run_conversation(self, user_message: str) -> str:
        """Run a single turn of conversation."""
        logger.info(f"Processing user message: {user_message[:100]}...")

        messages = [{"role": "user", "content": user_message}]

        while True:
            # Call Claude with tools
            response = self.client.messages.create(
                model="claude-opus-4-6",
                max_tokens=4096,
                system=self.system_prompt,
                tools=self.all_tools,
                messages=messages,
            )

            logger.info(f"Claude response - Stop reason: {response.stop_reason}")

            # Check if we're done
            if response.stop_reason == "end_turn":
                # Extract the final text response
                final_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_text = block.text
                        break
                return final_text

            # Process tool calls
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_result = self.process_tool_call(block.name, block.input)
                    logger.info(f"Tool result for {block.name}: {tool_result[:100]}...")
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": tool_result,
                        }
                    )

            # If no tool calls were made, extract text and return
            if not tool_results:
                final_text = ""
                for block in response.content:
                    if hasattr(block, "text"):
                        final_text = block.text
                        break
                return final_text

            # Add assistant response and tool results to messages
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

    def run_interactive(self):
        """Run the agent in interactive mode."""
        logger.info("Starting interactive agent mode. Type 'quit' to exit.")
        print(
            f"\n{'=' * 60}\n"
            f"Bem-vindo ao {self.settings.agent_name}\n"
            f"{'=' * 60}\n"
            f"Digite 'sair' ou 'quit' para terminar\n"
        )

        while True:
            try:
                user_input = input("\nVocê: ").strip()

                if user_input.lower() in ("sair", "quit", "exit"):
                    print("Até logo!")
                    break

                if not user_input:
                    continue

                response = self.run_conversation(user_input)
                print(f"\nAgente: {response}")

            except KeyboardInterrupt:
                print("\n\nAté logo!")
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {str(e)}")
                print(f"Erro: {str(e)}")

    def check_overdue_quotas(self) -> str:
        """Check and report overdue quotas."""
        logger.info("Checking overdue quotas...")
        message = (
            "Por favor, verifica se há quotas atrasadas e envia lembretes aos moradores "
            "que têm pagamentos em atraso há mais de 30 dias. Sê educado e construtivo."
        )
        return self.run_conversation(message)

    def check_open_incidents(self) -> str:
        """Check and report on open incidents."""
        logger.info("Checking open incidents...")
        message = (
            "Por favor, verifica quais são os incidentes abertos há mais de 15 dias "
            "e toma nota deles, preparando um sumário para o administrador."
        )
        return self.run_conversation(message)

    def process_emails(self) -> str:
        """Process and respond to emails."""
        logger.info("Processing emails...")
        message = (
            "Por favor, lê os emails não lidos do endereço do condomínio e responde "
            "com mensagens apropriadas, registando qualquer questão ou incidente relevante."
        )
        return self.run_conversation(message)


def main():
    """Main entry point."""
    try:
        # Initialize agent
        agent = CondominiumAgent()

        # Run interactive mode by default
        agent.run_interactive()

    except Exception as e:
        logger.error(f"Fatal error: {str(e)}")
        raise


if __name__ == "__main__":
    main()
