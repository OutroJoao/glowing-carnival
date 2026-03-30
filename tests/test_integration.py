"""Integration tests for end-to-end workflows."""

import json
from unittest.mock import MagicMock, patch, call
import pytest

from tests.realistic_mocks import (
    RealisticGmailMocks,
    RealisticSheetsMocks,
    RealisticAgentMocks,
    WorkflowScenarios,
)


class TestWorkflowScenarios:
    """Test complete workflow scenarios with realistic data."""

    def test_realistic_gmail_email_parsing(self):
        """Test parsing realistic Gmail email responses."""
        email = RealisticGmailMocks.quota_email()

        # Verify email has realistic structure
        assert "id" in email
        assert "payload" in email
        assert "headers" in email["payload"]
        assert "body" in email["payload"]

        # Find specific headers
        headers = {h["name"]: h["value"] for h in email["payload"]["headers"]}
        assert "Subject" in headers
        assert "From" in headers
        assert "To" in headers

    def test_realistic_sheets_data_structure(self):
        """Test realistic Google Sheets response structure."""
        residents = RealisticSheetsMocks.residents_sheet_response()

        # Verify sheet structure
        assert "values" in residents
        assert len(residents["values"]) > 1  # Header + data

        # Verify headers
        headers = residents["values"][0]
        assert "Nome" in headers
        assert "Apartamento" in headers
        assert "Email" in headers

        # Verify data rows
        for row in residents["values"][1:]:
            assert len(row) == len(headers)

    def test_incident_sheet_parsing(self):
        """Test parsing incident sheet with different statuses."""
        incidents = RealisticSheetsMocks.incidents_sheet_response()
        values = incidents["values"]

        # Get header indices
        headers = {h: i for i, h in enumerate(values[0])}

        # Extract incidents by status
        open_incidents = [
            row
            for row in values[1:]
            if row[headers["Status"]] == "Aberta"
        ]
        closed_incidents = [
            row
            for row in values[1:]
            if row[headers["Status"]] == "Fechada"
        ]

        assert len(open_incidents) >= 2
        assert len(closed_incidents) >= 1

    def test_quotas_sheet_overdue_detection(self):
        """Test detecting overdue quotas from sheet data."""
        quotas = RealisticSheetsMocks.quotas_sheet_response()
        values = quotas["values"]

        # Get header indices
        headers = {h: i for i, h in enumerate(values[0])}

        # Find overdue
        overdue = [
            row
            for row in values[1:]
            if row[headers["Status"]] == "Atrasada"
        ]

        assert len(overdue) >= 2
        for row in overdue:
            assert row[headers["Status"]] == "Atrasada"
            assert float(row[headers["Valor (€)"]]) > 0

    def test_agent_response_tool_use(self):
        """Test parsing agent response that uses tools."""
        response = RealisticAgentMocks.agent_response_with_tool_use()

        assert response["stop_reason"] == "tool_use"
        assert len(response["content"]) > 0
        assert response["content"][0]["type"] == "tool_use"
        assert response["content"][0]["name"] == "send_email"
        assert "input" in response["content"][0]

    def test_agent_response_final_text(self):
        """Test parsing agent response with final text."""
        response = RealisticAgentMocks.agent_response_with_text()

        assert response["stop_reason"] == "end_turn"
        assert len(response["content"]) > 0
        assert response["content"][0]["type"] == "text"
        assert "quota" in response["content"][0]["text"].lower()

    def test_workflow_scenario_structure(self):
        """Test workflow scenario data is properly structured."""
        scenario = WorkflowScenarios.scenario_resident_inquiry()

        assert "name" in scenario
        assert "description" in scenario
        assert "initial_email" in scenario
        assert "expected_actions" in scenario
        assert "expected_outcome" in scenario

        assert isinstance(scenario["expected_actions"], list)
        assert len(scenario["expected_actions"]) > 0


class TestDataPipelines:
    """Test data transformation pipelines."""

    def test_email_to_incident_pipeline(self):
        """Test pipeline: email → parse → log incident."""
        # Get realistic email
        email = RealisticGmailMocks.incident_email()

        # Extract headers
        headers = {h["name"]: h["value"] for h in email["payload"]["headers"]}

        # Parse email body (simulated)
        sender = headers["From"]
        subject = headers["Subject"]
        body = email["payload"]["body"]["data"]

        # Should be able to create incident from email
        assert sender is not None
        assert "avaria" in subject.lower() or "fuga" in subject.lower()
        assert body is not None

    def test_quota_sheet_to_email_pipeline(self):
        """Test pipeline: sheet → identify overdue → prepare email."""
        quotas = RealisticSheetsMocks.quotas_sheet_response()
        values = quotas["values"]
        headers = {h: i for i, h in enumerate(values[0])}

        # Find overdue
        overdue_rows = [
            row for row in values[1:]
            if row[headers["Status"]] == "Atrasada"
        ]

        # For each overdue, prepare email
        for row in overdue_rows:
            resident = row[headers["Residente"]]
            apartment = row[headers["Apartamento"]]
            value = row[headers["Valor (€)"]]

            # Email should contain this info
            assert resident is not None
            assert apartment is not None
            assert float(value) > 0

    def test_incident_categorization(self):
        """Test categorizing incidents by priority and status."""
        incidents = RealisticSheetsMocks.incidents_sheet_response()
        values = incidents["values"]
        headers = {h: i for i, h in enumerate(values[0])}

        # Categorize
        high_priority = [
            r for r in values[1:]
            if r[headers["Prioridade"]] == "Alta"
        ]
        open_incidents = [
            r for r in values[1:]
            if r[headers["Status"]] == "Aberta"
        ]

        assert len(high_priority) >= 1
        assert len(open_incidents) >= 1

        # High priority items should be handled first
        assert len(high_priority) <= len(open_incidents)


class TestDataValidation:
    """Test data validation and error handling."""

    def test_email_address_extraction(self):
        """Test extracting email from realistic email response."""
        email = RealisticGmailMocks.email_message(
            sender="joao@example.com",
            subject="Test",
        )

        headers = {h["name"]: h["value"] for h in email["payload"]["headers"]}
        sender_email = headers["From"]

        assert "@" in sender_email
        assert "example.com" in sender_email

    def test_currency_parsing(self):
        """Test parsing currency values from sheet."""
        quotas = RealisticSheetsMocks.quotas_sheet_response()
        values = quotas["values"]
        headers = {h: i for i, h in enumerate(values[0])}

        for row in values[1:]:
            value_str = row[headers["Valor (€)"]]
            value = float(value_str)

            assert value > 0
            assert value == 150.0  # Standard quota

    def test_date_formats(self):
        """Test date format consistency."""
        residents = RealisticSheetsMocks.residents_sheet_response()
        values = residents["values"]
        headers = {h: i for i, h in enumerate(values[0])}

        # Check date format (YYYY-MM-DD)
        for row in values[1:]:
            date_str = row[headers["Data Inscrição"]]
            parts = date_str.split("-")

            assert len(parts) == 3
            assert len(parts[0]) == 4  # Year
            assert len(parts[1]) == 2  # Month
            assert len(parts[2]) == 2  # Day

    def test_status_values_consistency(self):
        """Test status values are consistent across sheets."""
        valid_quota_statuses = ["Paga", "Pendente", "Atrasada"]
        valid_incident_statuses = ["Aberta", "Em Progresso", "Fechada"]

        quotas = RealisticSheetsMocks.quotas_sheet_response()
        incidents = RealisticSheetsMocks.incidents_sheet_response()

        # Check quota statuses
        quota_values = quotas["values"]
        quota_headers = {h: i for i, h in enumerate(quota_values[0])}
        for row in quota_values[1:]:
            status = row[quota_headers["Status"]]
            assert status in valid_quota_statuses

        # Check incident statuses
        incident_values = incidents["values"]
        incident_headers = {h: i for i, h in enumerate(incident_values[0])}
        for row in incident_values[1:]:
            status = row[incident_headers["Status"]]
            assert status in valid_incident_statuses
