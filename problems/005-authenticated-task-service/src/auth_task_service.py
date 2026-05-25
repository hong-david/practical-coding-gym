class AuthTaskService:
    def register_user(self, email: str, password: str) -> dict:
        raise NotImplementedError
    def login(self, email: str, password: str) -> str:
        raise NotImplementedError
    def create_task(self, token: str, title: str, description: str = "") -> dict:
        raise NotImplementedError
    def list_tasks(self, token: str) -> list[dict]:
        raise NotImplementedError
    def get_task(self, token: str, task_id: int) -> dict:
        raise NotImplementedError
    def update_task(self, token: str, task_id: int, **updates) -> dict:
        raise NotImplementedError
    def delete_task(self, token: str, task_id: int) -> bool:
        raise NotImplementedError
