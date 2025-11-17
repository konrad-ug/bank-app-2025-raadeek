class Account:
    def __init__(self):
        self.balance = 0.0
        
    def incoming_transfer(self, money):
        self.balance += money
        return self.balance
            

    def outgoing_transfer(self, money) -> bool:
        if self.balance >= money:
            self.balance -= money
            return True
        return False
    

    
