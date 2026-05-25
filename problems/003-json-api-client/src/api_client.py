class APIClientError(Exception):
    pass

class TransientAPIError(APIClientError):
    pass

class PermanentAPIError(APIClientError):
    pass

class BadResponseError(APIClientError):
    pass

class APIClient:
    def __init__(self, transport, max_retries=3):
        raise NotImplementedError

    def fetch_all_items(self, endpoint: str) -> list[dict]:
        raise NotImplementedError

    def fetch_item(self, endpoint: str, item_id: str) -> dict:
        raise NotImplementedError
