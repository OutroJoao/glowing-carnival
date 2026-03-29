"""Tests for Google Sheets tools."""

import json
from unittest.mock import MagicMock, patch
import pytest

from src.tools.sheets_tools import SheetsClient


class TestSheetsClient:
    """Test SheetsClient class."""

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_read_sheet(self, mock_exists, mock_build, test_settings, mock_sheets_service):
        """Test reading from a sheet."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                data = sheets.read_sheet(
                    spreadsheet_id="test-id",
                    sheet_name="Residents",
                )

                assert len(data) == 3  # Header + 2 rows
                assert data[0] == ["Nome", "Apartamento", "Email"]

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_read_sheet_with_range(
        self, mock_exists, mock_build, test_settings, mock_sheets_service
    ):
        """Test reading specific range from sheet."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                data = sheets.read_sheet(
                    spreadsheet_id="test-id",
                    sheet_name="Residents",
                    range_notation="A1:C2",
                )

                assert len(data) > 0

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_write_sheet(self, mock_exists, mock_build, test_settings, mock_sheets_service):
        """Test writing to a sheet."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                updated = sheets.write_sheet(
                    spreadsheet_id="test-id",
                    sheet_name="Residents",
                    range_notation="A1",
                    values=[["João", "101"]],
                )

                assert updated == 3

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_append_row(self, mock_exists, mock_build, test_settings, mock_sheets_service):
        """Test appending a row."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                updated_range = sheets.append_row(
                    spreadsheet_id="test-id",
                    sheet_name="Incidents",
                    row=["2024-03-29", "João Silva", "Teste"],
                )

                assert updated_range == "Incidents!A1"

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_get_residents(
        self, mock_exists, mock_build, test_settings, mock_sheets_service
    ):
        """Test getting residents list."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                residents = sheets.get_residents()

                assert len(residents) == 2
                assert residents[0]["Nome"] == "João Silva"
                assert residents[1]["Apartamento"] == "102"

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_get_overdue_quotas(
        self, mock_exists, mock_build, test_settings, mock_sheets_service
    ):
        """Test getting overdue quotas."""
        # Setup mock for overdue quotas
        mock_sheets_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
            "values": [
                ["Residente", "Apartamento", "Valor", "Status"],
                ["João Silva", "101", "150.00", "Atrasada"],
                ["Maria Santos", "102", "150.00", "Paga"],
                ["Carlos Oliveira", "201", "150.00", "Atrasada"],
            ]
        }

        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                overdue = sheets.get_overdue_quotas()

                assert len(overdue) == 2
                assert all(q["Status"] == "Atrasada" for q in overdue)

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_log_incident(self, mock_exists, mock_build, test_settings, mock_sheets_service):
        """Test logging an incident."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                updated = sheets.log_incident(
                    resident="João Silva",
                    description="Teste incidente",
                    priority="Normal",
                    status="Aberta",
                )

                assert updated == "Incidents!A1"

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_get_incidents(self, mock_exists, mock_build, test_settings, mock_sheets_service):
        """Test getting incidents."""
        # Setup mock for incidents
        mock_sheets_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
            "values": [
                ["Data", "Residente", "Descrição", "Status"],
                ["2024-03-25", "João Silva", "Fuga", "Aberta"],
                ["2024-03-20", "Maria", "Infiltração", "Fechada"],
            ]
        }

        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                incidents = sheets.get_incidents()

                assert len(incidents) == 2

    @patch("src.tools.sheets_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_get_incidents_filtered(
        self, mock_exists, mock_build, test_settings, mock_sheets_service
    ):
        """Test getting incidents filtered by status."""
        mock_sheets_service.spreadsheets.return_value.values.return_value.get.return_value.execute.return_value = {
            "values": [
                ["Data", "Residente", "Status"],
                ["2024-03-25", "João Silva", "Aberta"],
                ["2024-03-20", "Maria", "Fechada"],
            ]
        }

        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                sheets = SheetsClient(test_settings)
                sheets.service = mock_sheets_service

                open_incidents = sheets.get_incidents(status="Aberta")

                assert len(open_incidents) == 1
                assert open_incidents[0]["Status"] == "Aberta"
