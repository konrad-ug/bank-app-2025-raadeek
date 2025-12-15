from src.personal_account import PersonalAccount

class AccountsRegistry:
    def __init__(self):
        self.accounts = []

    def add_account(self, account: PersonalAccount):
        self.accounts.append(account)

    def find_by_pesel(self, pesel: str):
        for acc in self.accounts:
            if acc.pesel == pesel:
                return acc
        return None

    def get_all_accounts(self):
        return self.accounts

    def count_accounts(self):
        return len(self.accounts)

    def delete_account(self, pesel: str) -> bool:
        acc = self.find_by_pesel(pesel)
        if acc is None:
            return False
        self.accounts.remove(acc)
        return True