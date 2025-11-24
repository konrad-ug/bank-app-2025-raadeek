import pytest
from src.personal_account import PersonalAccount
from src.accounts_registry import AccountsRegistry


@pytest.fixture
def registry():
    return AccountsRegistry()


@pytest.fixture
def sample_accounts():
    return [
        PersonalAccount("John", "Doe", "67010112345"),
        PersonalAccount("Jane", "Smith", "80010112345"),
        PersonalAccount("Adam", "Nowak", "90010112345")
    ]


def test_add_and_count_accounts(registry, sample_accounts):
    for acc in sample_accounts:
        registry.add_account(acc)

    assert registry.count_accounts() == 3


def test_get_all_accounts(registry, sample_accounts):
    for acc in sample_accounts:
        registry.add_account(acc)

    assert registry.get_all_accounts() == sample_accounts


def test_find_by_pesel(registry, sample_accounts):
    acc1 = sample_accounts[1]
    registry.add_account(acc1)

    result = registry.find_by_pesel(acc1.pesel)
    assert result is acc1


def test_find_by_pesel_not_found(registry):
    assert registry.find_by_pesel("00000000000") is None
