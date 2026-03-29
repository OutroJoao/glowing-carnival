"""Google Sheets integration tools for the condominium agent."""

from typing import List, Dict, Any, Optional
import os
import pickle

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery

from src.config.settings import Settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


class SheetsClient:
    """Client for Google Sheets API operations."""

    def __init__(self, settings: Settings):
        """Initialize Sheets client."""
        self.settings = settings
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Google Sheets API."""
        creds_path = self.settings.get_credentials_path()
        token_path = self.settings.get_token_path()

        creds = None

        # Load existing token if available
        if os.path.exists(token_path):
            with open(token_path, "rb") as token_file:
                creds = pickle.load(token_file)

        # If no valid credentials, authenticate
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(creds_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {creds_path}. "
                        "Please download it from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save credentials for future use
            with open(token_path, "wb") as token_file:
                pickle.dump(creds, token_file)

        self.service = discovery.build("sheets", "v4", credentials=creds)

    def read_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        range_notation: Optional[str] = None,
    ) -> List[List[Any]]:
        """
        Read data from a sheet.

        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet name
            range_notation: Optional range (e.g., "A1:D10")

        Returns:
            List of rows
        """
        if range_notation:
            range_name = f"{sheet_name}!{range_notation}"
        else:
            range_name = sheet_name

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(spreadsheetId=spreadsheet_id, range=range_name)
                .execute()
            )
            return result.get("values", [])
        except Exception as e:
            raise Exception(f"Failed to read sheet: {str(e)}")

    def write_sheet(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        range_notation: str,
        values: List[List[Any]],
    ) -> int:
        """
        Write data to a sheet.

        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet name
            range_notation: Range to write to (e.g., "A1")
            values: List of rows to write

        Returns:
            Number of updated cells
        """
        range_name = f"{sheet_name}!{range_notation}"
        body = {"values": values}

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .update(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            return result.get("updatedCells", 0)
        except Exception as e:
            raise Exception(f"Failed to write to sheet: {str(e)}")

    def append_row(
        self,
        spreadsheet_id: str,
        sheet_name: str,
        row: List[Any],
    ) -> str:
        """
        Append a row to a sheet.

        Args:
            spreadsheet_id: Google Sheets ID
            sheet_name: Sheet name
            row: Row data to append

        Returns:
            Updated range
        """
        range_name = f"{sheet_name}!A:Z"
        body = {"values": [row]}

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .append(
                    spreadsheetId=spreadsheet_id,
                    range=range_name,
                    valueInputOption="USER_ENTERED",
                    body=body,
                )
                .execute()
            )
            return result.get("updates", {}).get("updatedRange", "")
        except Exception as e:
            raise Exception(f"Failed to append row: {str(e)}")

    def get_residents(self) -> List[Dict[str, Any]]:
        """Get all residents from the residents sheet."""
        rows = self.read_sheet(
            self.settings.residents_sheet_id,
            self.settings.residents_sheet_name,
        )

        if not rows:
            return []

        headers = rows[0]
        residents = []

        for row in rows[1:]:
            resident = {}
            for i, header in enumerate(headers):
                resident[header] = row[i] if i < len(row) else ""
            residents.append(resident)

        return residents

    def get_overdue_quotas(self) -> List[Dict[str, Any]]:
        """Get all overdue quotas from the quotas sheet."""
        rows = self.read_sheet(
            self.settings.quotas_sheet_id,
            self.settings.quotas_sheet_name,
        )

        if not rows:
            return []

        headers = rows[0]
        overdue = []

        for row in rows[1:]:
            quota = {}
            for i, header in enumerate(headers):
                quota[header] = row[i] if i < len(row) else ""

            # Check if quota is overdue (assuming "Status" column exists)
            if quota.get("Status", "").lower() == "atrasada":
                overdue.append(quota)

        return overdue

    def log_incident(
        self,
        resident: str,
        description: str,
        priority: str = "Normal",
        status: str = "Aberta",
    ) -> str:
        """
        Log a new incident.

        Args:
            resident: Resident name or apartment
            description: Incident description
            priority: Priority level
            status: Current status

        Returns:
            Updated range
        """
        from datetime import datetime

        row = [datetime.now().isoformat(), resident, description, priority, status]
        return self.append_row(
            self.settings.incidents_sheet_id,
            self.settings.incidents_sheet_name,
            row,
        )

    def get_incidents(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get incidents from the incidents sheet.

        Args:
            status: Filter by status (e.g., "Aberta", "Fechada")

        Returns:
            List of incidents
        """
        rows = self.read_sheet(
            self.settings.incidents_sheet_id,
            self.settings.incidents_sheet_name,
        )

        if not rows:
            return []

        headers = rows[0]
        incidents = []

        for row in rows[1:]:
            incident = {}
            for i, header in enumerate(headers):
                incident[header] = row[i] if i < len(row) else ""

            if status is None or incident.get("Status", "") == status:
                incidents.append(incident)

        return incidents
