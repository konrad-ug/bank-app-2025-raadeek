from src.personal_account import PersonalAccount

class TestPesel:
    def test_pesel_too_long(self):
        account = PersonalAccount("John", "Doe", "123456789012")
        assert account.pesel == "Invalid"
        assert account.balance == 0.0


    def test_pesel_too_short(self):
        account = PersonalAccount("John", "Doe", "1234567890")  
        assert account.pesel == "Invalid"
        assert account.balance == 0.0
    
    def test_pesel_non_numeric(self):
        account = PersonalAccount("John", "Doe", "12345abc901")  
        assert account.pesel == "Invalid"
        assert account.balance == 0.0

