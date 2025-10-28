from src.account import Account

class TestTransfer:

    def test_incoming_transfer(self):
        account = Account()
        account.incoming_transfer(100.0)
        assert account.balance == 100

    def test_outgoing_transfer(self):
        account = Account()
        account.balance = 100.0
        account.outgoing_transfer(100.0)
        assert account.balance == 0

    def test_outgoing_transfer_suffiecient_balance(self):
        account = Account()
        account.balance = 100.0
        account.outgoing_transfer(40.0)
        assert account.balance == 60

    def test_outgoing_transfer_insufficenit_balance(self):
        account = Account()
        account.incoming_transfer(100.0)
        account.outgoing_transfer(150.0)
        assert account.balance == -50
