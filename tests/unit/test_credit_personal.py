import pytest
from src.personal_account import PersonalAccount


@pytest.fixture
def personal_account():
    return PersonalAccount("John", "Doe", "67010112345")


class TestCreditPersonal:
    @pytest.mark.parametrize(
        "operations, credit, expected_granted",
        [
            ([100.0, 150.0, 200.0], 200.0, True),
            ([100.0, -50.0, 200.0], 200.0, False),
        ],
    )
    def test_submit_for_loan_last_three_deposits(
        self, personal_account, operations, credit, expected_granted
    ):
        for amount in operations:
            if amount > 0:
                personal_account.incoming_transfer(amount)
            else:
                personal_account.outgoing_transfer(-amount)

        starting_balance = personal_account.balance

        result = personal_account.submit_for_loan(credit)

        assert result is expected_granted
        if expected_granted:
            assert personal_account.balance == starting_balance + credit
        else:
            assert personal_account.balance == starting_balance

    @pytest.mark.parametrize(
        "operations, credit, expected_granted",
        [
            ([10.0, 20.0, 50.0, 50.0, 50.0, 50.0, 60.0], 200.0, True),
            ([10.0, 20.0, 50.0, 50.0, 50.0, 20.0, 30.0], 200.0, True),
        ],
    )
    def test_submit_for_loan_sum_of_last_five(
        self, personal_account, operations, credit, expected_granted
    ):
        for amount in operations:
            if amount > 0:
                personal_account.incoming_transfer(amount)
            else:
                personal_account.outgoing_transfer(-amount)

        starting_balance = personal_account.balance

        result = personal_account.submit_for_loan(credit)

        assert result is expected_granted
        if expected_granted:
            assert personal_account.balance == starting_balance + credit
        else:
            assert personal_account.balance == starting_balance

    def test_submit_for_loan_not_granted_when_no_history(self, personal_account):
        result = personal_account.submit_for_loan(200.0)

        assert result is False
        assert personal_account.balance == 0.0
