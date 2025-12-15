import pytest
from src.personal_account import PersonalAccount


class TestPromoCodeValidation:
    """Unit tests for is_promo_code_valid method"""
    
    def test_is_promo_code_valid_none(self):
        """Test is_promo_code_valid with None"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid(None) is False
    
    def test_is_promo_code_valid_correct(self):
        """Test is_promo_code_valid with valid code"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("PROM_12a") is True
    
    def test_is_promo_code_valid_wrong_prefix(self):
        """Test is_promo_code_valid with wrong prefix"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("XXXX_12a") is False
    
    def test_is_promo_code_valid_wrong_length(self):
        """Test is_promo_code_valid with wrong length"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_promo_code_valid("PROM_1234") is False


class TestAgeValidation:
    """Unit tests for is_age_valid method"""
    
    def test_is_age_valid_invalid_pesel(self):
        """Test is_age_valid with invalid PESEL"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("12345") is False
    
    def test_is_age_valid_valid_month_1(self):
        """Test is_age_valid with valid month (1-12)"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("67010112345") is True
    
    def test_is_age_valid_valid_month_2(self):
        """Test is_age_valid with valid month (21-32) from 2000s"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("85211212345") is True
    
    def test_is_age_valid_invalid_month(self):
        """Test is_age_valid with invalid month (> 32)"""
        account = PersonalAccount("John", "Doe", "80010112345")
        assert account.is_age_valid("67451112345") is False
    
    def test_is_age_valid_too_old(self):
        """Test is_age_valid with PESEL indicating person born before 1960"""
        account = PersonalAccount("John", "Doe", "80010112345")
        # PESEL 09 + month 01 = 1909, which is < 1960
        assert account.is_age_valid("09010112345") is False
