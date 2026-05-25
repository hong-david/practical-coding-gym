class APIError(Exception):
    pass


def create_app(task_store=None):
    raise NotImplementedError


class InMemoryTaskStore:
    def create_project(self, name: str) -> dict:
        raise NotImplementedError

    def list_projects(self) -> list:
        raise NotImplementedError

    def create_task(self, project_id: int, title: str, status: str = "todo") -> dict:
        raise NotImplementedError

    def list_tasks(self, project_id=None, status=None) -> list:
        raise NotImplementedError

    def update_task(self, task_id: int, **updates) -> dict:
        raise NotImplementedError

    def delete_task(self, task_id: int) -> bool:
        raise NotImplementedError
