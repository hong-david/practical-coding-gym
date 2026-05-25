class ThreadSafeLedger:
    def __init__(self):
        raise NotImplementedError

    def create_account(self, account_id: str, initial_balance=0) -> dict:
        raise NotImplementedError

    def deposit(self, account_id: str, amount) -> dict:
        raise NotImplementedError

    def withdraw(self, account_id: str, amount) -> dict:
        raise NotImplementedError

    def transfer(self, from_account_id: str, to_account_id: str, amount) -> dict:
        raise NotImplementedError

    def get_balance(self, account_id: str):
        raise NotImplementedError

    def snapshot(self) -> dict:
        raise NotImplementedError
