import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import date
from src.personal_account import PersonalAccount
from src.company_account import Company_Account
from smtp.smtp import SMTPClient


class TestPersonalAccountSendHistoryViaEmail:

    @patch('src.personal_account.SMTPClient')
    def test_send_history_email_success_personal_account(self, mock_smtp_class):
        # Arrange
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = PersonalAccount("John", "Doe", "12345678901", "PROM_1234")
        account.incoming_transfer(100)
        account.outgoing_transfer(1)
        account.incoming_transfer(500)

        # Act
        result = account.send_history_via_email("test@example.com")

        # Assert
        assert result is True
        mock_smtp_instance.send.assert_called_once()

    @patch('src.personal_account.SMTPClient')
    def test_send_history_email_failure_personal_account(self, mock_smtp_class):
        # Arrange
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance

        account = PersonalAccount("John", "Doe", "12345678901", "PROM_1234")
        account.incoming_transfer(100)

        # Act
        result = account.send_history_via_email("test@example.com")

        # Assert
        assert result is False
        mock_smtp_instance.send.assert_called_once()

    @patch('src.personal_account.SMTPClient')
    def test_send_history_email_personal_account_correct_params(self, mock_smtp_class):
        # Arrange
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = PersonalAccount("John", "Doe", "12345678901", "PROM_1234")
        account.history = [100.0, -1.0, 500.0]
        test_email = "john@example.com"

        # Act
        account.send_history_via_email(test_email)

        # Assert
        call_args = mock_smtp_instance.send.call_args
        assert call_args is not None
        
        subject, text, email_address = call_args[0]
        
        # Check email address
        assert email_address == test_email
        
        # Check subject format
        today = date.today().isoformat()
        assert subject == f"Account Transfer History {today}"
        
        # Check text content
        assert text == "Personal account history: [100.0, -1.0, 500.0]"

    @patch('src.personal_account.SMTPClient')
    def test_send_history_email_personal_account_empty_history(self, mock_smtp_class):
        # Arrange
        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = PersonalAccount("Jane", "Smith", "12345678901", "PROM_5678")

        # Act
        result = account.send_history_via_email("jane@example.com")

        # Assert
        assert result is True
        call_args = mock_smtp_instance.send.call_args
        subject, text, email_address = call_args[0]
        assert text == "Personal account history: []"


class TestCompanyAccountSendHistoryViaEmail:

    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    def test_send_history_email_success_company_account(self, mock_smtp_class, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_requests_get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = Company_Account("Test Company", "1234567890")
        account.incoming_transfer(5000)
        account.outgoing_transfer(1000)
        account.incoming_transfer(500)

        # Act
        result = account.send_history_via_email("company@example.com")

        # Assert
        assert result is True
        mock_smtp_instance.send.assert_called_once()

    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    def test_send_history_email_failure_company_account(self, mock_smtp_class, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_requests_get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = False
        mock_smtp_class.return_value = mock_smtp_instance

        account = Company_Account("Test Company", "1234567890")
        account.incoming_transfer(5000)

        # Act
        result = account.send_history_via_email("company@example.com")

        # Assert
        assert result is False
        mock_smtp_instance.send.assert_called_once()

    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    def test_send_history_email_company_account_correct_params(self, mock_smtp_class, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_requests_get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = Company_Account("Test Company", "1234567890")
        account.history = [5000.0, -1000.0, 500.0]
        test_email = "company@example.com"

        # Act
        account.send_history_via_email(test_email)

        # Assert
        call_args = mock_smtp_instance.send.call_args
        assert call_args is not None
        
        subject, text, email_address = call_args[0]
        
        # Check email address
        assert email_address == test_email
        
        # Check subject format
        today = date.today().isoformat()
        assert subject == f"Account Transfer History {today}"
        
        # Check text content
        assert text == "Company account history: [5000.0, -1000.0, 500.0]"

    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    def test_send_history_email_company_account_empty_history(self, mock_smtp_class, mock_requests_get):
        """Test email sending when company account has no history"""
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_requests_get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        account = Company_Account("Test Company", "1234567890")

        # Act
        result = account.send_history_via_email("company@example.com")

        # Assert
        assert result is True
        call_args = mock_smtp_instance.send.call_args
        subject, text, email_address = call_args[0]
        assert text == "Company account history: []"

    @patch('src.company_account.requests.get')
    @patch('src.company_account.SMTPClient')
    def test_send_history_email_company_account_mocks_nip_verification(self, mock_smtp_class, mock_requests_get):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'result': {
                'subject': {
                    'statusVat': 'Czynny'
                }
            }
        }
        mock_requests_get.return_value = mock_response

        mock_smtp_instance = MagicMock()
        mock_smtp_instance.send.return_value = True
        mock_smtp_class.return_value = mock_smtp_instance

        # Act
        account = Company_Account("Test Company", "1234567890")
        account.send_history_via_email("company@example.com")

        # Assert
        assert mock_requests_get.called
        mock_smtp_instance.send.assert_called_once()
