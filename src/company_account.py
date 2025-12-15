from src.account import Account
import os
import requests
from datetime import date


class Company_Account(Account):
    def __init__(self, company_name, nip):
        super().__init__()
        self.company_name = company_name

        # If NIP has wrong length, accept but mark as Invalid and skip verification
        if not self.valid_nip(nip):
            self.nip = "Invalid"
            return

        # For valid-length NIP, verify against MF registry
        verified = self.verify_nip_with_mf(nip)
        if not verified:
            raise ValueError("Company not registered!!")

        self.nip = nip

    def valid_nip(self, nip):
        return len(nip) == 10 and nip.isdigit()

    def verify_nip_with_mf(self, nip: str) -> bool:
        """Call MF API to verify NIP. Returns True if statusVat == 'Czynny'.

        Prints response JSON to logs for visibility.
        Uses env var BANK_APP_MF_URL with a default test URL.
        """
        base = os.environ.get("BANK_APP_MF_URL", "https://wl-test.mf.gov.pl")
        today = date.today().isoformat()
        url = f"{base.rstrip('/')}/api/search/nip/{nip}?date={today}"

        try:
            resp = requests.get(url, timeout=10)
            # Attempt to parse JSON; print raw text if parse fails
            try:
                j = resp.json()
            except Exception:
                print(f"MF response (non-json): {resp.text}")
                return False

            print(f"MF response: {j}")

            # The API returns a structure that includes 'result' or direct fields.
            # Try to find statusVat in known locations.
            status = None
            if isinstance(j, dict):
                # common pattern: j.get('result', {}).get('subject', {}).get('statusVat')
                if 'result' in j:
                    try:
                        status = j['result']['subject']['statusVat']
                    except Exception:
                        status = None
                # fallback: direct 'statusVat'
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
    