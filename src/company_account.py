from src.account import Account

class Company_Account(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name
        self.nip = nip if self.valid_nip(nip) else "Invalid"


    def valid_nip(self, nip):
        return len(nip) == 10 and nip.isdigit()
    