from src.account import Account

class PersonalAccount(Account):
    def __init__(self, first_name, last_name, pesel, promo_code=None):
        super().__init__() # ustawia balance = 0.0
        self.first_name = first_name
        self.last_name = last_name

        self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"

        if (
            self.is_pesel_valid(pesel)
            and self.is_promo_code_valid(promo_code)
            and self.is_age_valid(pesel)
        ):
            self.balance += 50.0  

    def is_pesel_valid(self, pesel):
        return len(pesel) == 11 and pesel.isdigit()
    
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        return promo_code.startswith("PROM_") and len(promo_code) == 8
    
    def is_age_valid(self, pesel):

        if not self.is_pesel_valid(pesel):
            return False

        rr = int(pesel[0:2])
        mm = int(pesel[2:4])

        if 1 <= mm <= 12:
            year = 1900 + rr
        elif 21 <= mm <= 32:
            year = 2000 + rr
        else:
            return False
    
        return year > 1960
    
    def express_outgoing_transfer(self, money) -> bool:
        return super().express_outgoing_transfer(money, fee = 1.0)