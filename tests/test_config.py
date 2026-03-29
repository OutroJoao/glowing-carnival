"""Tests for configuration module."""

import pytest
from pathlib import Path
from src.config.settings import Settings


class TestSettings:
    """Test Settings class."""

    def test_settings_load_from_env(self, test_settings):
        """Test loading settings from environment."""
        assert test_settings.anthropic_api_key == "test-key-12345"
        assert test_settings.gmail_sender_address == "test@condominio.pt"
        assert test_settings.agent_name == "Agente de Teste"
        assert test_settings.agent_language == "pt_PT"

    def test_settings_sheet_ids(self, test_settings):
        """Test sheet ID configuration."""
        assert test_settings.residents_sheet_id == "test-residents-id"
        assert test_settings.incidents_sheet_id == "test-incidents-id"
        assert test_settings.quotas_sheet_id == "test-quotas-id"

    def test_settings_sheet_names(self, test_settings):
        """Test sheet name configuration."""
        assert test_settings.residents_sheet_name == "Residents"
        assert test_settings.incidents_sheet_name == "Incidents"
        assert test_settings.quotas_sheet_name == "Quotas"

    def test_get_credentials_path(self, test_settings):
        """Test getting credentials file path."""
        path = test_settings.get_credentials_path()
        assert isinstance(path, Path)
        assert path.name == "credentials.json"

    def test_get_token_path(self, test_settings):
        """Test getting token file path."""
        path = test_settings.get_token_path()
        assert isinstance(path, Path)
        assert path.name == "token.json"

    def test_settings_defaults(self, test_settings):
        """Test that defaults are properly set."""
        # These should use the provided values in conftest
        assert test_settings.gmail_credentials_file == "credentials.json"
        assert test_settings.gmail_token_file == "token.json"

    def test_settings_required_fields(self, temp_env_file):
        """Test that missing required fields raise error."""
        # Create env file with missing API key
        env_content = """
GMAIL_CREDENTIALS_FILE=credentials.json
RESIDENTS_SHEET_ID=test-id
INCIDENTS_SHEET_ID=test-id
QUOTAS_SHEET_ID=test-id
"""
        temp_env_file.write_text(env_content.strip())

        with pytest.raises(Exception):  # Should raise validation error
            Settings(_env_file=str(temp_env_file))
