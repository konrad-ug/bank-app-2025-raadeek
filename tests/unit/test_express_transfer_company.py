from src.company_account import Company_Account


class TestExpressTransferCompany:
    def test_company_express_allows_small_debit_equal_to_fee(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(200.0)

        result = account.express_outgoing_transfer(200.0)

        assert result is True
        assert account.balance == -5.0

    def test_company_express_requires_enough_for_amount(self):
        account = Company_Account("Nokia", "1234567890")
        account.incoming_transfer(100.0)

        result = account.express_outgoing_transfer(150.0)

        assert result is False
        assert account.balance == 100.0
