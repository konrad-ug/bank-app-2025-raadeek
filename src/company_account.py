class Company_Account:
    def __init__(self, company_name, nip):
        self.company_name = company_name
        self.nip = nip if self.valid_nip(nip) else "invalid"


    def valid_nip(self, nip):
        if len(nip) == 10 and nip.isdigit():
            return True
        else:
            return False
    