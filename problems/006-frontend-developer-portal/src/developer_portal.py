def login(api, email: str, password: str) -> dict:
    raise NotImplementedError
def auth_headers(token: str) -> dict:
    raise NotImplementedError
def create_initial_state() -> dict:
    raise NotImplementedError
def reducer(state: dict, action: dict) -> dict:
    raise NotImplementedError
def fetch_all_pages(api, path: str) -> list[dict]:
    raise NotImplementedError
def update_resource(api, token: str, resource_id: str, updates: dict) -> dict:
    raise NotImplementedError
