from abc import ABC, abstractmethod


class AccountsRepository(ABC):
    """Abstract interface for accounts persistence"""
    
    @abstractmethod
    def save_all(self, accounts):
        """Save all accounts to repository"""
        pass
    
    @abstractmethod
    def load_all(self):
        """Load all accounts from repository"""
        pass
