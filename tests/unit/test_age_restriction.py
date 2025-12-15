from src.personal_account import PersonalAccount

class Test_Age_Restriction:
    def test_age_not_valid(self):
        account = PersonalAccount("John", "Doe", "44010112345", "PROM_123")
        assert account.balance == 0.0

    def test_age_valid(self):
        account = PersonalAccount("John", "Doe", "67055678911", "PROM_123")
        assert account.balance == 50.0

    def test_age_invalid_month(self):
        """Test PESEL with invalid month (mm > 32)"""
        account = PersonalAccount("John", "Doe", "67455678911", "PROM_123")
        assert account.balance == 0.0  # Invalid month means no promo bonus