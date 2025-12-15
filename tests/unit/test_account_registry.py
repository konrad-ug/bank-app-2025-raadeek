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


def test_add_account_duplicate_pesel(registry):
    """Test that adding account with duplicate PESEL fails"""
    pesel = "89092909825"
    
    # Add first account
    account1 = PersonalAccount("james", "hetfield", pesel)
    success1, message1 = registry.add_account(account1)
    
    assert success1 is True
    assert message1 == "Account added successfully"
    assert registry.count_accounts() == 1
    
    # Try to add second account with same PESEL
    account2 = PersonalAccount("lars", "ulrich", pesel)
    success2, message2 = registry.add_account(account2)
    
    assert success2 is False
    assert message2 == "PESEL already exists"
    assert registry.count_accounts() == 1  # Still only 1 account


def test_add_account_unique_pesels(registry):
    """Test adding multiple accounts with different PESELs"""
    account1 = PersonalAccount("james", "hetfield", "89092909825")
    account2 = PersonalAccount("lars", "ulrich", "85010112345")
    account3 = PersonalAccount("kirk", "hammett", "82111412345")
    
    success1, _ = registry.add_account(account1)
    success2, _ = registry.add_account(account2)
    success3, _ = registry.add_account(account3)
    
    assert success1 is True
    assert success2 is True
    assert success3 is True
    assert registry.count_accounts() == 3
