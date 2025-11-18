from src.personal_account import PersonalAccount


class TestExpressTransferPersonal:
    def test_personal_express_allows_small_debit_equal_to_fee(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        account.incoming_transfer(50.0)

        result = account.express_outgoing_transfer(50.0)

        assert result is True
        assert account.balance == -1.0

    def test_personal_express_requires_enough_for_amount(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        account.incoming_transfer(50.0)

        result = account.express_outgoing_transfer(60.0)
        assert result is False
        assert account.balance == 50.0

    def test_personal_express_when_enough_for_all(self):
        account = PersonalAccount("John", "Doe", "67010112345")
        account.incoming_transfer(100.0)

        result = account.express_outgoing_transfer(50.0)

        assert result is True
        assert account.balance == 49.0
