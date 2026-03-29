"""Gmail integration tools for the condominium agent."""

import os
import base64
import pickle
from typing import Optional, List, Dict, Any
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.api_python_client import discovery
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from src.config.settings import Settings

# Gmail API scopes
SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


class GmailClient:
    """Client for Gmail API operations."""

    def __init__(self, settings: Settings):
        """Initialize Gmail client."""
        self.settings = settings
        self.service = None
        self._authenticate()

    def _authenticate(self) -> None:
        """Authenticate with Gmail API."""
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

        self.service = discovery.build("gmail", "v1", credentials=creds)

    def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
    ) -> str:
        """
        Send an email.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text or HTML
            html: Whether body is HTML
            cc: List of CC recipients
            bcc: List of BCC recipients

        Returns:
            Message ID
        """
        message = MIMEMultipart("alternative")
        message["to"] = to
        message["subject"] = subject

        if cc:
            message["cc"] = ", ".join(cc)
        if bcc:
            message["bcc"] = ", ".join(bcc)

        mime_type = "html" if html else "plain"
        message.attach(MIMEText(body, mime_type, "utf-8"))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            result = self.service.users().messages().send(
                userId="me", body={"raw": raw_message}
            ).execute()
            return result["id"]
        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

    def read_emails(
        self,
        query: str = "is:unread",
        max_results: int = 10,
    ) -> List[Dict[str, Any]]:
        """
        Read emails from inbox.

        Args:
            query: Gmail search query
            max_results: Maximum number of emails to retrieve

        Returns:
            List of email data
        """
        try:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", q=query, maxResults=max_results)
                .execute()
            )

            messages = results.get("messages", [])
            emails = []

            for message in messages:
                msg = (
                    self.service.users()
                    .messages()
                    .get(userId="me", id=message["id"], format="full")
                    .execute()
                )
                emails.append(self._parse_message(msg))

            return emails
        except Exception as e:
            raise Exception(f"Failed to read emails: {str(e)}")

    def _parse_message(self, message: Dict[str, Any]) -> Dict[str, Any]:
        """Parse email message from Gmail API response."""
        headers = message["payload"]["headers"]
        body = ""

        if "parts" in message["payload"]:
            for part in message["payload"]["parts"]:
                if part["mimeType"] == "text/plain":
                    data = part["body"].get("data", "")
                    body = base64.urlsafe_b64decode(data).decode("utf-8")
                    break
        else:
            data = message["payload"]["body"].get("data", "")
            if data:
                body = base64.urlsafe_b64decode(data).decode("utf-8")

        parsed = {
            "id": message["id"],
            "threadId": message["threadId"],
            "subject": next(
                (h["value"] for h in headers if h["name"] == "Subject"), ""
            ),
            "from": next((h["value"] for h in headers if h["name"] == "From"), ""),
            "to": next((h["value"] for h in headers if h["name"] == "To"), ""),
            "date": next((h["value"] for h in headers if h["name"] == "Date"), ""),
            "body": body,
        }

        return parsed

    def reply_to_email(
        self,
        thread_id: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> str:
        """
        Reply to an email in a thread.

        Args:
            thread_id: Gmail thread ID
            subject: Reply subject
            body: Reply body
            html: Whether body is HTML

        Returns:
            Message ID
        """
        message = MIMEMultipart("alternative")
        message["subject"] = subject

        mime_type = "html" if html else "plain"
        message.attach(MIMEText(body, mime_type, "utf-8"))

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        try:
            result = (
                self.service.users()
                .messages()
                .send(
                    userId="me",
                    body={"raw": raw_message, "threadId": thread_id},
                )
                .execute()
            )
            return result["id"]
        except Exception as e:
            raise Exception(f"Failed to reply to email: {str(e)}")

    def mark_as_read(self, message_id: str) -> None:
        """Mark email as read."""
        try:
            self.service.users().messages().modify(
                userId="me", id=message_id, body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        except Exception as e:
            raise Exception(f"Failed to mark email as read: {str(e)}")
