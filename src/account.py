class Account:
    def __init__(self):
        self.balance = 0.0
        self.history = []  

    def incoming_transfer(self, money: float):
        self.balance += money
        self.history.append(float(money))
        return self.balance

    def outgoing_transfer(self, money: float) -> bool:
        if self.balance >= money:
            self.balance -= money
            self.history.append(-float(money))
            return True
        return False

    def express_outgoing_transfer(self, money: float, fee: float) -> bool:
        if not self.outgoing_transfer(money):
            return False

        self.balance -= fee
        self.history.append(-float(fee))
        return True
