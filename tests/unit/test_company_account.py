from src.company_account import Company_Account
from src.account import Account

class Test_Company_Account:
    def test_company_nip(self):
        account = Company_Account("Nokia", "1234567")
        assert account.nip == "invalid"

    def test_company_account(self):
        account = Company_Account("Nokia", "1234567890")
        assert account.company_name == "Nokia"
        assert account.nip == "1234567890"

    def test_company_transfer(self):
        account = Account()
        account.incoming_transfer(100.0)
        assert account.balance == 100

    def test_outgoing_transfer(self):
        account = Account()
        account.balance = 100.0
        account.outgoing_transfer(100.0)
        assert account.balance == 0