import pytest
from src.personal_account import PersonalAccount


class TestPromoCodeValidation:
    
    def test_is_promo_code_valid_none(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid(None) is False
    
    def test_is_promo_code_valid_correct(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("PROM_12a") is True
    
    def test_is_promo_code_valid_wrong_prefix(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("XXXX_12a") is False
    
    def test_is_promo_code_valid_wrong_length(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("PROM_1234") is False


class TestAgeValidation:
    
    def test_is_age_valid_invalid_pesel(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("12345") is False
    
    def test_is_age_valid_valid_month_1(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("67010112345") is True
    
    def test_is_age_valid_valid_month_2(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("85211212345") is True
    
    def test_is_age_valid_invalid_month(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("67451112345") is False
    
    def test_is_age_valid_too_old(self):
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("09010112345") is False
