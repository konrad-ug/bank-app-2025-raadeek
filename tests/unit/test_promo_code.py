import pytest
from src.personal_account import PersonalAccount


@pytest.fixture
def base_pesel():
    return "67010112345"  # poprawny PESEL dla uproszczenia


@pytest.mark.parametrize(
    "pesel, promo_code, expected_balance",
    [
        ("67010112345", "PROM_12a", 50.0),   # poprawny kod (8 chars)
        ("12345678911", "1_2345678", 0.0),   # zły format
        ("12345678911", "PAOM_123", 0.0),    # zły prefix
        ("12345678911", "PROM_1234", 0.0),   # zła długość
        ("67010112345", None, 0.0),          # brak kodu
        ("67010112345", "PROM_ABC", 50.0),   # valid promo code (8 chars)
    ],
)
def test_promo_codes(pesel, promo_code, expected_balance):
    account = PersonalAccount("John", "Doe", pesel, promo_code)
    assert account.balance == expected_balance
