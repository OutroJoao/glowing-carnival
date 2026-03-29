"""Settings and configuration for the condominium agent."""

from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = ConfigDict(env_file=".env", case_sensitive=False)

    # Claude API
    anthropic_api_key: str = Field(..., alias="ANTHROPIC_API_KEY")

    # Gmail Configuration
    gmail_credentials_file: str = Field(
        default="credentials.json", alias="GMAIL_CREDENTIALS_FILE"
    )
    gmail_token_file: str = Field(default="token.json", alias="GMAIL_TOKEN_FILE")
    gmail_sender_address: str = Field(
        default="condominio@example.com", alias="GMAIL_SENDER_ADDRESS"
    )

    # Google Sheets Configuration
    sheets_credentials_file: str = Field(
        default="credentials.json", alias="SHEETS_CREDENTIALS_FILE"
    )
    residents_sheet_id: str = Field(..., alias="RESIDENTS_SHEET_ID")
    residents_sheet_name: str = Field(default="Residents", alias="RESIDENTS_SHEET_NAME")
    incidents_sheet_id: str = Field(..., alias="INCIDENTS_SHEET_ID")
    incidents_sheet_name: str = Field(default="Incidents", alias="INCIDENTS_SHEET_NAME")
    quotas_sheet_id: str = Field(..., alias="QUOTAS_SHEET_ID")
    quotas_sheet_name: str = Field(default="Quotas", alias="QUOTAS_SHEET_NAME")

    # Agent Configuration
    agent_name: str = Field(
        default="Agente de Gestão Condominial", alias="AGENT_NAME"
    )
    agent_language: str = Field(default="pt_PT", alias="AGENT_LANGUAGE")

    def get_credentials_path(self) -> Path:
        """Get the absolute path to credentials file."""
        return Path(self.gmail_credentials_file).absolute()

    def get_token_path(self) -> Path:
        """Get the absolute path to token file."""
        return Path(self.gmail_token_file).absolute()
