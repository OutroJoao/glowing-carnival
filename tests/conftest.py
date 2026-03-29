"""Pytest configuration and shared fixtures."""

import os
import json
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
import pytest

from src.config.settings import Settings


@pytest.fixture
def temp_env_file(tmp_path):
    """Create a temporary .env file for testing."""
    env_file = tmp_path / ".env"
    env_content = """
ANTHROPIC_API_KEY=test-key-12345
GMAIL_CREDENTIALS_FILE=credentials.json
GMAIL_TOKEN_FILE=token.json
GMAIL_SENDER_ADDRESS=test@condominio.pt
SHEETS_CREDENTIALS_FILE=credentials.json
RESIDENTS_SHEET_ID=test-residents-id
RESIDENTS_SHEET_NAME=Residents
INCIDENTS_SHEET_ID=test-incidents-id
INCIDENTS_SHEET_NAME=Incidents
QUOTAS_SHEET_ID=test-quotas-id
QUOTAS_SHEET_NAME=Quotas
AGENT_NAME=Agente de Teste
AGENT_LANGUAGE=pt_PT
"""
    env_file.write_text(env_content.strip())
    return env_file


@pytest.fixture
def test_settings(temp_env_file, monkeypatch):
    """Create Settings instance for testing."""
    monkeypatch.chdir(temp_env_file.parent)
    return Settings(_env_file=str(temp_env_file))


@pytest.fixture
def mock_gmail_service():
    """Mock Gmail API service."""
    service = MagicMock()

    # Mock users().messages().list()
    service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [
            {
                "id": "msg-1",
                "threadId": "thread-1"
            }
        ]
    }

    # Mock users().messages().get()
    service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "id": "msg-1",
        "threadId": "thread-1",
        "payload": {
            "headers": [
                {"name": "Subject", "value": "Test Subject"},
                {"name": "From", "value": "sender@example.com"},
                {"name": "To", "value": "test@example.com"},
                {"name": "Date", "value": "Mon, 29 Mar 2024 10:00:00"},
            ],
            "body": {"data": ""}
        }
    }

    # Mock users().messages().send()
    service.users.return_value.messages.return_value.send.return_value.execute.return_value = {
        "id": "msg-new-1"
    }

    # Mock users().messages().modify()
    service.users.return_value.messages.return_value.modify.return_value.execute.return_value = {}

    return service


@pytest.fixture
def mock_sheets_service():
    """Mock Google Sheets API service."""
    service = MagicMock()

    # Mock spreadsheets().values().get()
    service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
        "values": [
            ["Nome", "Apartamento", "Email"],
            ["João Silva", "101", "joao@example.com"],
            ["Maria Santos", "102", "maria@example.com"],
        ]
    }

    # Mock spreadsheets().values().update()
    service.spreadsheets.return_value.values.return_value.update.return_value.execute.return_value = {
        "updatedCells": 3
    }

    # Mock spreadsheets().values().append()
    service.spreadsheets.return_value.values.return_value.append.return_value.execute.return_value = {
        "updates": {"updatedRange": "Incidents!A1"}
    }

    return service


@pytest.fixture
def mock_credentials():
    """Mock Google OAuth credentials."""
    creds = MagicMock()
    creds.valid = True
    creds.expired = False
    creds.refresh_token = None
    return creds


@pytest.fixture
def sample_email():
    """Sample email data."""
    return {
        "id": "msg-1",
        "threadId": "thread-1",
        "subject": "Quota de Março",
        "from": "joao@example.com",
        "to": "condominio@example.com",
        "date": "Mon, 29 Mar 2024 10:00:00",
        "body": "Quando vence a quota de março?",
    }


@pytest.fixture
def sample_residents():
    """Sample residents data."""
    return [
        {
            "Nome": "João Silva",
            "Apartamento": "101",
            "Email": "joao@example.com",
            "Telefone": "918888888",
            "Data Inscrição": "2024-01-15",
        },
        {
            "Nome": "Maria Santos",
            "Apartamento": "102",
            "Email": "maria@example.com",
            "Telefone": "919999999",
            "Data Inscrição": "2024-01-15",
        },
    ]


@pytest.fixture
def sample_overdue_quotas():
    """Sample overdue quotas."""
    return [
        {
            "Residente": "João Silva",
            "Apartamento": "101",
            "Valor (€)": "150.00",
            "Data Vencimento": "2024-02-10",
            "Status": "Atrasada",
            "Mês/Ano": "Fevereiro 2024",
        },
        {
            "Residente": "Carlos Oliveira",
            "Apartamento": "201",
            "Valor (€)": "150.00",
            "Data Vencimento": "2024-02-10",
            "Status": "Atrasada",
            "Mês/Ano": "Fevereiro 2024",
        },
    ]


@pytest.fixture
def sample_incidents():
    """Sample incidents."""
    return [
        {
            "Data": "2024-03-25",
            "Residente": "João Silva",
            "Descrição": "Torneira com fuga",
            "Prioridade": "Normal",
            "Status": "Aberta",
            "Notas": "Contactado encanador",
        },
        {
            "Data": "2024-03-20",
            "Residente": "Maria Santos",
            "Descrição": "Infiltração no teto",
            "Prioridade": "Alta",
            "Status": "Em Progresso",
            "Notas": "Obra iniciada",
        },
    ]
