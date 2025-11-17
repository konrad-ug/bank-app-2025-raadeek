from src.personal_account import PersonalAccount


class TestPromoCode:
    def test_promo_code_valid(self):
        account = PersonalAccount("John", "Doe", "67010112345", "PROM_12a")
        assert account.balance == 50.0
    

    def test_promo_code_invalid_format(self):
        account = PersonalAccount("John", "Doe", "12345678911", "1_2345678")
        assert account.balance == 0.0

    def test_promo_code_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "12345678911", "PAOM_123")
        assert account.balance == 0.0

    def test_promo_code_wrong_suffix(self):
        account = PersonalAccount("John", "Doe", "12345678911", "PROM_1234")
        assert account.balance == 0.0

    def test_promo_code_wrong_suffix_too_long(self):
        account = PersonalAccount("John", "Doe", "67010112345", "PROM_1234")  
        assert account.balance == 0.0


    def test_promo_code_wrong_suffix_too_short(self):
        account = PersonalAccount("John", "Doe", "12345678911", "PROM_1234")
        assert account.balance == 0.0

    def test_no_promo_code(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        assert account.balance == 0.0