from src.account import Account
import os
import requests
from datetime import date
from smtp.smtp import SMTPClient


class Company_Account(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name

        if not self.valid_nip(nip):
            self.nip = "Invalid"
            return

        verified = self.verify_nip_with_mf(nip)
        if not verified:
            raise ValueError("Company not registered!!")

        self.nip = nip

    def valid_nip(self, nip):
        return len(nip) == 10 and nip.isdigit()

    def verify_nip_with_mf(self, nip: str) -> bool:
        base = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().isoformat()
        url = f"{base.rstrip('/')}/api/search/nip/{nip}?date={today}"

        try:
            resp = requests.get(url, timeout=10)
            try:
                j = resp.json()
            except Exception:
                print(f"MF response (non-json): {resp.text}")
                return False

            print(f"MF response: {j}")

            status = None
            if isinstance(j, dict):
                if 'result' in j:
                    try:
                        status = j['result']['subject']['statusVat']
                    except Exception:
                        status = None
                if status is None and 'statusVat' in j:
                    status = j.get('statusVat')

            return status == "Czynny"
        except Exception as e:
            print(f"Error calling MF API: {e}")
            return False

    def express_outgoing_transfer(self, money) -> bool:
        return super().express_outgoing_transfer(money, fee = 5.0)

    def take_loan(self, amount: float) -> bool:
        condition_balance = self.balance >= 2 * amount

        condition_zus = -1775.0 in self.history

        if condition_balance and condition_zus:
            self.balance += amount
            return True

        return False

    def send_history_via_email(self, email_address: str) -> bool:
        """
        Send account transfer history via email
        
        Args:
            email_address: Recipient email address
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        today = date.today().isoformat()
        subject = f"Account Transfer History {today}"
        text = f"Company account history: {self.history}"
        
        smtp_client = SMTPClient()
        return smtp_client.send(subject, text, email_address)