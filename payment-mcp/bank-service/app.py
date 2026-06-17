from payment_engine import bank


if __name__ == "__main__":
    print("Dummy Bank Service sample")
    print(bank.get_balance("101"))
    print(bank.create_payment("101", "999", 1000))
    print(bank.payment_status("PAY-0001"))
