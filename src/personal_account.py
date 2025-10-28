class PersonalAccount:
    def __init__(self, first_name, last_name, pesel, promo_code=None):
            self.first_name = first_name
            self.last_name = last_name
            self.balance = 50.0 if self.is_promo_code_valid(promo_code) else 0.0
            self.pesel = pesel if self.is_pesel_valid(pesel) else "Invalid"
            self.balance = 50.0 if self.is_age_valid(pesel) else 0.0    

    def is_pesel_valid(self, pesel):
        if len(pesel) == 11 and pesel.isdigit():
            return True
        return False
    
    def is_promo_code_valid(self, promo_code):
        if promo_code is None:
            return False
        if promo_code and promo_code.startswith("PROM_") and len(promo_code) == 8:
            return True
        return False
    
    def is_age_valid(self, pesel):
        rr = int(pesel[0:2])
        mm = int(pesel[2:4])

        if 1 <= mm <= 12:
            year = 1900 + rr
        elif 21 <= mm <= 32:
            year = 2000 + rr
        else:
            return False
    
        return year > 1960
    