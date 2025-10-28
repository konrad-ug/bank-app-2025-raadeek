from src.personal_account import PersonalAccount

class Test_Age_Restriction:
    def test_age_not_valid(self):
        account = PersonalAccount("John", "Doe", "44055678911", "PROM_1234")
        assert account.balance == 0.0
    def test_age_valid(self):
        account = PersonalAccount("John", "Doe", "67055678911", "PROM_1234")
        assert account.balance == 50.0