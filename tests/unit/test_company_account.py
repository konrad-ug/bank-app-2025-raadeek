from src.company_account import Company_Account

class Test_Company_Account:

    def test_company_nip_invalid(self):
        account = Company_Account("Nokia", "1234567")  
        assert account.nip == "Invalid"

    def test_company_account_valid_nip(self):
        account = Company_Account("Nokia", "1234567890")
        assert account.company_name == "Nokia"
        assert account.nip == "1234567890"
        assert account.balance == 0.0

    def test_company_account(self):
        account = Company_Account("Nokia", "1234567890")
        assert account.company_name == "Nokia"
        assert account.nip == "1234567890"

    def test_company_incoming_transfer(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(100.0)
        assert account.balance == 100.0

    def test_company_outgoing_transfer(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(100.0)

        result = account.outgoing_transfer(60.0)

        assert result is True
        assert account.balance == 40.0

    def test_company_outgoing_transfer_insufficient_balance(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(50.0)

        result = account.outgoing_transfer(100.0)

        assert result is False
        assert account.balance == 50.0