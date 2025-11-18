from src.account import Account
from src.personal_account import PersonalAccount
from src.company_account import Company_Account


class TestAccountHistory:
    def test_history_starts_empty(self):
        account = Account()
        assert account.history == []

    def test_incoming_transfer_recorded_in_history(self):
        account = Account()
        account.incoming_transfer(500.0)
        assert account.history == [500.0]

    def test_outgoing_transfer_recorded_in_history(self):
        account = Account()
        account.incoming_transfer(500.0)

        result = account.outgoing_transfer(200.0)

        assert result is True
        assert account.history == [500.0, -200.0]

    def test_outgoing_transfer_not_recorded_when_insufficient_balance(self):
        account = Account()
        account.incoming_transfer(100.0)

        result = account.outgoing_transfer(200.0)

        assert result is False
        assert account.history == [100.0]


class TestExpressTransferHistory:
    def test_personal_express_transfer_history(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        account.incoming_transfer(500.0)

        result = account.express_outgoing_transfer(300.0)

        assert result is True
        assert account.history == [500.0, -300.0, -1.0]

    def test_company_express_transfer_history(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(500.0)

        result = account.express_outgoing_transfer(300.0)

        assert result is True
        assert account.history == [500.0, -300.0, -5.0]

    def test_express_transfer_not_recorded_when_insufficient_balance(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        account.incoming_transfer(100.0)

        result = account.express_outgoing_transfer(200.0)

        assert result is False
        assert account.history == [100.0]
