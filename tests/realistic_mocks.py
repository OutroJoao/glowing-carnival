"""Realistic mock data matching actual Google API formats."""

import json
from datetime import datetime, timedelta
from typing import List, Dict, Any


class RealisticGmailMocks:
    """Realistic Gmail API response data."""

    @staticmethod
    def unread_email_response() -> Dict[str, Any]:
        """Realistic Gmail unread emails list response."""
        return {
            "messages": [
                {"id": "18c1b1a7e8c2b3a4", "threadId": "18c1b1a7e8c2b3a4"},
                {"id": "18c1b1a7e8c2b3a5", "threadId": "18c1b1a7e8c2b3a5"},
            ],
            "resultSizeEstimate": 2,
        }

    @staticmethod
    def email_message(
        sender: str = "joao@example.com",
        subject: str = "Quota de Março",
        body: str = "Quando vence a quota de março?",
    ) -> Dict[str, Any]:
        """Realistic Gmail message with full payload."""
        import base64

        return {
            "id": "18c1b1a7e8c2b3a4",
            "threadId": "18c1b1a7e8c2b3a4",
            "labelIds": ["UNREAD", "INBOX"],
            "snippet": body[:100],
            "payload": {
                "mimeType": "text/plain",
                "filename": "",
                "headers": [
                    {"name": "Return-Path", "value": f"<{sender}>"},
                    {"name": "Received", "value": "from mail-ed1-x.example.com"},
                    {"name": "DKIM-Signature", "value": "v=1; a=rsa-sha256;"},
                    {"name": "MIME-Version", "value": "1.0"},
                    {"name": "From", "value": sender},
                    {"name": "Date", "value": "Mon, 29 Mar 2024 10:30:00 +0100"},
                    {"name": "Message-ID", "value": "<abc123@example.com>"},
                    {"name": "Subject", "value": subject},
                    {"name": "To", "value": "condominio@example.com"},
                    {"name": "Content-Type", "value": "text/plain; charset=UTF-8"},
                ],
                "body": {"size": len(body), "data": base64.urlsafe_b64encode(body.encode()).decode()},
            },
            "sizeEstimate": 1500,
            "historyId": "1234567890",
            "internalDate": "1711700400000",
        }

    @staticmethod
    def quota_email() -> Dict[str, Any]:
        """Resident asking about quota."""
        return RealisticGmailMocks.email_message(
            sender="maria@example.com",
            subject="Dúvida sobre quota",
            body="Bom dia,\n\nGostaria de saber quando vence a quota de março e se posso pagar atrasada.\n\nObrigada,\nMaria Santos\nApartamento 102",
        )

    @staticmethod
    def incident_email() -> Dict[str, Any]:
        """Resident reporting an incident."""
        return RealisticGmailMocks.email_message(
            sender="joao@example.com",
            subject="Avaria - Fuga de água",
            body="Olá,\n\nA minha cozinha tem uma fuga de água na torneira principal. Podem vir reparar?\n\nApartamento 101\nJoão Silva",
        )

    @staticmethod
    def send_email_response() -> Dict[str, Any]:
        """Gmail send email successful response."""
        return {
            "id": "18c1b1a8f9d3c4e5",
            "threadId": "18c1b1a8f9d3c4e5",
            "labelIds": ["SENT"],
        }


class RealisticSheetsMocks:
    """Realistic Google Sheets API response data."""

    @staticmethod
    def residents_sheet_response() -> Dict[str, Any]:
        """Realistic residents sheet data."""
        return {
            "range": "Residents!A1:E6",
            "majorDimension": "ROWS",
            "values": [
                ["Nome", "Apartamento", "Email", "Telefone", "Data Inscrição"],
                ["João Silva", "101", "joao@example.com", "918888888", "2024-01-15"],
                ["Maria Santos", "102", "maria@example.com", "919999999", "2024-01-15"],
                ["Carlos Oliveira", "201", "carlos@example.com", "916666666", "2024-02-01"],
                ["Ana Costa", "202", "ana@example.com", "917777777", "2024-02-01"],
                ["Pedro Ferreira", "301", "pedro@example.com", "915555555", "2024-03-01"],
            ],
        }

    @staticmethod
    def quotas_sheet_response() -> Dict[str, Any]:
        """Realistic quotas sheet with mixed statuses."""
        today = datetime.now()
        last_month = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        next_month = (today + timedelta(days=15)).strftime("%Y-%m-%d")

        return {
            "range": "Quotas!A1:F8",
            "majorDimension": "ROWS",
            "values": [
                ["Residente", "Apartamento", "Valor (€)", "Data Vencimento", "Status", "Mês/Ano"],
                ["João Silva", "101", "150.00", today.strftime("%Y-%m-%d"), "Paga", "Março 2024"],
                ["Maria Santos", "102", "150.00", last_month, "Atrasada", "Fevereiro 2024"],
                ["Carlos Oliveira", "201", "150.00", today.strftime("%Y-%m-%d"), "Pendente", "Março 2024"],
                ["Ana Costa", "202", "150.00", today.strftime("%Y-%m-%d"), "Paga", "Março 2024"],
                ["Pedro Ferreira", "301", "150.00", last_month, "Atrasada", "Fevereiro 2024"],
                ["Maria Santos", "102", "150.00", next_month, "Pendente", "Abril 2024"],
            ],
        }

    @staticmethod
    def incidents_sheet_response() -> Dict[str, Any]:
        """Realistic incidents sheet."""
        return {
            "range": "Incidents!A1:F5",
            "majorDimension": "ROWS",
            "values": [
                ["Data", "Residente", "Descrição", "Prioridade", "Status", "Notas"],
                ["2024-03-25", "João Silva", "Torneira com fuga na cozinha", "Normal", "Aberta", "Contactado encanador"],
                ["2024-03-20", "Maria Santos", "Infiltração no teto da sala", "Alta", "Em Progresso", "Obra já iniciada"],
                ["2024-03-10", "Carlos Oliveira", "Luz da escada com avaria", "Baixa", "Aberta", "Agendado reparação"],
                ["2024-02-15", "Ana Costa", "Campainha não funciona", "Normal", "Fechada", "Reparado em 22/02"],
            ],
        }

    @staticmethod
    def append_row_response() -> Dict[str, Any]:
        """Successful append row response."""
        return {
            "spreadsheetId": "test-sheet-id",
            "updatedRange": "Incidents!A6:F6",
            "updatedRows": 1,
            "updatedColumns": 6,
            "updatedCells": 6,
        }

    @staticmethod
    def write_response() -> Dict[str, Any]:
        """Successful write response."""
        return {
            "spreadsheetId": "test-sheet-id",
            "updatedRange": "Quotas!A2:F2",
            "updatedRows": 1,
            "updatedColumns": 6,
            "updatedCells": 6,
        }


class RealisticAgentMocks:
    """Realistic Claude Agent API responses."""

    @staticmethod
    def agent_response_with_tool_use(
        tool_name: str = "send_email",
        tool_input: Dict[str, Any] = None,
    ) -> Dict[str, Any]:
        """Agent response that uses a tool."""
        if tool_input is None:
            tool_input = {
                "to": "joao@example.com",
                "subject": "Resposta sobre quota",
                "body": "Olá João,\n\nSua quota de março vence em 31/03/2024.\n\nCumprimentos,\nAgente",
            }

        return {
            "id": "msg_xyz",
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "tool_use",
                    "id": "tool_123",
                    "name": tool_name,
                    "input": tool_input,
                }
            ],
            "model": "claude-opus-4-6",
            "stop_reason": "tool_use",
            "stop_sequence": None,
            "usage": {"input_tokens": 150, "output_tokens": 50},
        }

    @staticmethod
    def agent_response_with_text() -> Dict[str, Any]:
        """Agent response with final text (no tool use)."""
        return {
            "id": "msg_abc",
            "type": "message",
            "role": "assistant",
            "content": [
                {
                    "type": "text",
                    "text": "Identifiquei 2 quotas em atraso (João Silva e Pedro Ferreira). Vou enviar lembretes amáveis a ambos.",
                }
            ],
            "model": "claude-opus-4-6",
            "stop_reason": "end_turn",
            "usage": {"input_tokens": 200, "output_tokens": 60},
        }


class WorkflowScenarios:
    """Complete workflow scenario data."""

    @staticmethod
    def scenario_resident_inquiry() -> Dict[str, Any]:
        """Scenario: Resident inquires about quota."""
        return {
            "name": "Resident Quota Inquiry",
            "description": "Resident emails asking when quota is due",
            "initial_email": RealisticGmailMocks.quota_email(),
            "expected_actions": [
                "read_emails",
                "get_residents",
                "get_overdue_quotas",
                "send_email",
            ],
            "expected_outcome": "Email sent to resident with quota info",
        }

    @staticmethod
    def scenario_incident_report() -> Dict[str, Any]:
        """Scenario: Resident reports an incident."""
        return {
            "name": "Incident Report",
            "description": "Resident reports water leak",
            "initial_email": RealisticGmailMocks.incident_email(),
            "expected_actions": [
                "read_emails",
                "log_incident",
                "send_email",
            ],
            "expected_outcome": "Incident logged and resident confirmed",
        }

    @staticmethod
    def scenario_overdue_check() -> Dict[str, Any]:
        """Scenario: Check for overdue quotas and send reminders."""
        return {
            "name": "Overdue Quota Check",
            "description": "Agent checks for overdue quotas and sends reminders",
            "initial_action": "check_overdue_quotas",
            "expected_actions": [
                "get_overdue_quotas",
                "send_email",  # One for each overdue
                "send_email",
            ],
            "expected_outcome": "Reminders sent to 2 residents with overdue quotas",
        }

    @staticmethod
    def scenario_incident_followup() -> Dict[str, Any]:
        """Scenario: Follow up on old open incidents."""
        return {
            "name": "Incident Follow-up",
            "description": "Agent checks open incidents older than 15 days",
            "initial_action": "check_open_incidents",
            "expected_actions": [
                "get_incidents",
                "send_email",  # Update requests
            ],
            "expected_outcome": "Follow-up emails sent to residents with old incidents",
        }
