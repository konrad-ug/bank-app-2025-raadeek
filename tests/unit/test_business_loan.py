import pytest
from src.company_account import Company_Account

@pytest.fixture
def company():
    return Company_Account("Nokia", "1234567890")


@pytest.mark.parametrize(
    "initial_balance, history, loan_amount, expected",
    [
        
        (5000, [5000, -1775, 100], 1000, True),

       
        (5000, [100, 200, 300], 1000, False),

        
        (1500, [-1775], 1000, False),


        (500, [50, 20], 200, False),
    ]
)
def test_business_loan(company, initial_balance, history, loan_amount, expected):
    company.balance = initial_balance
    company.history = history.copy()

    result = company.take_loan(loan_amount)

    assert result is expected
    if expected:
        assert company.balance == initial_balance + loan_amount
    else:
        assert company.balance == initial_balance