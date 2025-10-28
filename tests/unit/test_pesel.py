from src.personal_account import PersonalAccount

class TestPesel:
    def test_pesel_too_length(self):
        account = PersonalAccount("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"


    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"

    
    def test_pesel_non_numeric(self):
        account = PersonalAccount("John", "Doe", "12345678911")
        assert account.pesel == "12345678911"

