class JobTimeoutError(Exception):
    pass


class ScheduledWorker:
    def __init__(self, clock, max_attempts: int = 3, default_timeout_seconds: int = 30):
        raise NotImplementedError

    def enqueue_at(self, job_type: str, payload: dict, run_at: float, timeout_seconds=None) -> dict:
        raise NotImplementedError

    def enqueue_in(self, job_type: str, payload: dict, delay_seconds: float, timeout_seconds=None) -> dict:
        raise NotImplementedError

    def cancel(self, job_id: int) -> bool:
        raise NotImplementedError

    def run_due(self, handlers: dict) -> list:
        raise NotImplementedError

    def get_job(self, job_id: int) -> dict:
        raise NotImplementedError

    def dead_letters(self) -> list:
        raise NotImplementedError
