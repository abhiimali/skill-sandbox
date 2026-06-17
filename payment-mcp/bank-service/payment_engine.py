from dataclasses import dataclass, asdict


@dataclass
class Account:
    account_id: str
    holder_name: str
    balance: float
    currency: str = "INR"


@dataclass
class Payment:
    payment_id: str
    from_account: str
    receiver_account: str
    amount: float
    currency: str
    status: str
    message: str


class DummyBankService:
    """Tiny in-memory bank used by MCP tools for learning."""

    def __init__(self) -> None:
        self.accounts = {
            "101": Account("101", "User Account", 10000.0),
            "999": Account("999", "Receiver Account", 2500.0),
        }
        self.payments: dict[str, Payment] = {}

    def get_balance(self, account_id: str) -> dict:
        account = self.accounts.get(account_id)
        if account is None:
            return {
                "ok": False,
                "status": "failed",
                "message": f"Account {account_id} was not found",
            }
        return {"ok": True, **asdict(account)}

    def create_payment(self, from_account: str, receiver_account: str, amount: float) -> dict:
        payment_id = f"PAY-{len(self.payments) + 1:04d}"
        source = self.accounts.get(from_account)
        receiver = self.accounts.get(receiver_account)

        if source is None:
            return self._record_payment(
                payment_id,
                from_account,
                receiver_account,
                amount,
                "failed",
                f"Sender account {from_account} was not found",
            )
        if receiver is None:
            return self._record_payment(
                payment_id,
                from_account,
                receiver_account,
                amount,
                "failed",
                f"Receiver account {receiver_account} was not found",
            )
        if amount <= 0:
            return self._record_payment(
                payment_id,
                from_account,
                receiver_account,
                amount,
                "failed",
                "Amount must be greater than zero",
            )
        if source.balance < amount:
            return self._record_payment(
                payment_id,
                from_account,
                receiver_account,
                amount,
                "failed",
                "Insufficient balance",
            )

        source.balance -= amount
        receiver.balance += amount
        return self._record_payment(
            payment_id,
            from_account,
            receiver_account,
            amount,
            "success",
            f"Payment from {from_account} to {receiver_account} completed",
        )

    def payment_status(self, payment_id: str) -> dict:
        payment = self.payments.get(payment_id)
        if payment is None:
            return {
                "ok": False,
                "status": "failed",
                "message": f"Payment {payment_id} was not found",
            }
        return {"ok": payment.status == "success", **asdict(payment)}

    def _record_payment(
        self,
        payment_id: str,
        from_account: str,
        receiver_account: str,
        amount: float,
        status: str,
        message: str,
    ) -> dict:
        payment = Payment(
            payment_id=payment_id,
            from_account=from_account,
            receiver_account=receiver_account,
            amount=amount,
            currency="INR",
            status=status,
            message=message,
        )
        self.payments[payment_id] = payment
        return {"ok": status == "success", **asdict(payment)}


bank = DummyBankService()
