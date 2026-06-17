import sys
from pathlib import Path


BANK_SERVICE_PATH = Path(__file__).resolve().parents[2] / "bank-service"
sys.path.insert(0, str(BANK_SERVICE_PATH))

from payment_engine import bank


def get_balance(account_id: str) -> dict:
    """Get account balance by calling the dummy bank service."""
    return bank.get_balance(account_id)
