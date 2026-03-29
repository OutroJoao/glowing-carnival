"""Tests for Gmail tools."""

import json
import base64
from unittest.mock import MagicMock, patch, Mock
import pytest

from src.tools.gmail_tools import GmailClient


class TestGmailClient:
    """Test GmailClient class."""

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("src.tools.gmail_tools.InstalledAppFlow")
    def test_authenticate_with_new_credentials(
        self, mock_flow, mock_build, test_settings, tmp_path
    ):
        """Test authentication flow with new credentials."""
        # Setup mocks
        mock_flow_instance = MagicMock()
        mock_flow.from_client_secrets_file.return_value = mock_flow_instance
        mock_creds = MagicMock()
        mock_flow_instance.run_local_server.return_value = mock_creds

        # Temporarily change home directory
        with patch("os.path.exists", return_value=False):
            with patch("builtins.open", create=True):
                with patch("pickle.dump"):
                    gmail = GmailClient(test_settings)

                    assert gmail.service is not None
                    mock_build.assert_called_once()

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_send_email(self, mock_exists, mock_build, test_settings, mock_gmail_service):
        """Test sending an email."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                message_id = gmail.send_email(
                    to="recipient@example.com",
                    subject="Test Subject",
                    body="Test Body",
                )

                assert message_id == "msg-new-1"
                mock_gmail_service.users.return_value.messages.return_value.send.assert_called_once()

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_send_email_with_html(
        self, mock_exists, mock_build, test_settings, mock_gmail_service
    ):
        """Test sending HTML email."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                message_id = gmail.send_email(
                    to="recipient@example.com",
                    subject="Test",
                    body="<h1>Test</h1>",
                    html=True,
                )

                assert message_id == "msg-new-1"

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_send_email_with_cc_bcc(
        self, mock_exists, mock_build, test_settings, mock_gmail_service
    ):
        """Test sending email with CC and BCC."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                message_id = gmail.send_email(
                    to="recipient@example.com",
                    subject="Test",
                    body="Test",
                    cc=["cc@example.com"],
                    bcc=["bcc@example.com"],
                )

                assert message_id == "msg-new-1"

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_read_emails(self, mock_exists, mock_build, test_settings, mock_gmail_service):
        """Test reading emails."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                emails = gmail.read_emails(query="is:unread", max_results=10)

                assert len(emails) > 0
                assert "id" in emails[0]
                assert "subject" in emails[0]

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_read_emails_empty(self, mock_exists, mock_build, test_settings, mock_gmail_service):
        """Test reading when no emails."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service
                mock_gmail_service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
                    "messages": []
                }

                emails = gmail.read_emails()

                assert emails == []

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_reply_to_email(
        self, mock_exists, mock_build, test_settings, mock_gmail_service
    ):
        """Test replying to email."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                message_id = gmail.reply_to_email(
                    thread_id="thread-1",
                    subject="Re: Original",
                    body="Reply text",
                )

                assert message_id == "msg-new-1"

    @patch("src.tools.gmail_tools.discovery.build")
    @patch("os.path.exists", return_value=False)
    def test_mark_as_read(self, mock_exists, mock_build, test_settings, mock_gmail_service):
        """Test marking email as read."""
        with patch("builtins.open", create=True):
            with patch("pickle.dump"):
                gmail = GmailClient(test_settings)
                gmail.service = mock_gmail_service

                gmail.mark_as_read("msg-1")

                mock_gmail_service.users.return_value.messages.return_value.modify.assert_called_once()
