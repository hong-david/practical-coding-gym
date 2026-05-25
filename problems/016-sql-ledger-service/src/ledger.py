class MigrationError(Exception):
    pass


def apply_migrations(db_path, migrations_dir) -> None:
    raise NotImplementedError


def initialize_database(db_path) -> None:
    raise NotImplementedError


class LedgerService:
    def __init__(self, db_path):
        raise NotImplementedError

    def create_account(self, name: str, currency: str) -> dict:
        raise NotImplementedError

    def get_account(self, account_id: int) -> dict:
        raise NotImplementedError

    def list_accounts(self) -> list:
        raise NotImplementedError

    def record_transfer(self, from_account_id: int, to_account_id: int, amount, idempotency_key: str) -> dict:
        raise NotImplementedError

    def get_balance(self, account_id: int):
        raise NotImplementedError

    def list_transactions(self, account_id=None) -> list:
        raise NotImplementedError
