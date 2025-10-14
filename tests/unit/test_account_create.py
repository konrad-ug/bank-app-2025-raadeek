from src.account import Account


class TestAccount:
    def test_account_creation(self):
        account = Account("John", "Doe", "12345678911")
        assert account.first_name == "John"
        assert account.last_name == "Doe"
        assert account.balance == 0.0
        assert account.pesel == "12345678911"

    def test_pesel_too_length(self):
        account = Account("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"


    def test_pesel_too_short(self):
        account = Account("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"

    
    def test_pesel_non_numeric(self):
        account = Account("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"
