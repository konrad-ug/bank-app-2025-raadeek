from pymongo import MongoClient
from src.accounts_repository import AccountsRepository
from src.personal_account import PersonalAccount


class MongoAccountsRepository(AccountsRepository):    
    def __init__(self, mongo_uri="mongodb://localhost:27017/", db_name="bank_app"):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[db_name]
        self._collection = self.db["accounts"]
    
    def save_all(self, accounts):
        self._collection.delete_many({})
        
        for account in accounts:
            self._collection.update_one(
                {"pesel": account.pesel},
                {"$set": account.to_dict()},
                upsert=True,
            )
    
    def load_all(self):
        accounts = []
        for account_data in self._collection.find():
            account = PersonalAccount(
                first_name=account_data["first_name"],
                last_name=account_data["last_name"],
                pesel=account_data["pesel"]
            )
            account.balance = account_data.get("balance", 0.0)
            account.history = account_data.get("history", [])
            accounts.append(account)
        
        return accounts
    
    def close(self):
        self.client.close()
