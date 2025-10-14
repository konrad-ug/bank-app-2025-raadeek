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



    def test_promo_code_valid(self):
        account = Account("John", "Doe", "12345678911", "PROM_12a")
        assert account.balance == 50.0
    

    def test_promo_code_invalid_format(self):
        account = Account("John", "Doe", "12345678911", "1_2345678")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = Account("John", "Doe", "12345678911", "PAOM_123")
        assert account.balance == 0.0

    def test_promo_code_wrong_suffix(self):
        account = Account("John", "Doe", "12345678911", "PROM_1234")
        assert account.balance == 0.0

    def test_promo_code_wrong_suffix_too_long(self):
        account = Account("John", "Doe", "12345678911", "PROM_1234")
        assert account.balance == 0.0


    def test_promo_code_wrong_suffix_too_short(self):
        account = Account("John", "Doe", "12345678911", "PROM_1234")
        assert account.balance == 0.0
