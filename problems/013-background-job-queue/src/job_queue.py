from typing import Optional


class JobQueue:
    def __init__(self, max_attempts: int = 3):
        raise NotImplementedError
    def enqueue(self, job_type: str, payload: dict) -> dict:
        raise NotImplementedError
    def reserve_next(self) -> Optional[dict]:
        raise NotImplementedError
    def complete(self, job_id: int) -> None:
        raise NotImplementedError
    def fail(self, job_id: int, reason: str) -> None:
        raise NotImplementedError
    def dead_letters(self) -> list[dict]:
        raise NotImplementedError
