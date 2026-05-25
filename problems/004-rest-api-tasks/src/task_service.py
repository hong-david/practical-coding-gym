from typing import Optional


class TaskService:
    def create_task(self, title: str, description: str = "", status: str = "todo") -> dict:
        raise NotImplementedError
    def get_task(self, task_id: int) -> dict:
        raise NotImplementedError
    def list_tasks(self, status: Optional[str] = None) -> list[dict]:
        raise NotImplementedError
    def update_task(self, task_id: int, **updates) -> dict:
        raise NotImplementedError
    def delete_task(self, task_id: int) -> bool:
        raise NotImplementedError
