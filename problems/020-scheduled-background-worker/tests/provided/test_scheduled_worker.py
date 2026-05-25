from pathlib import Path
import sys

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROBLEM_ROOT / "src"))

from scheduled_worker import JobTimeoutError, ScheduledWorker


class FakeClock:
    def __init__(self, now=0):
        self.current = now

    def now(self):
        return self.current

    def advance(self, seconds):
        self.current += seconds


def worker(**kwargs):
    return ScheduledWorker(FakeClock(), **kwargs)


def test_max_attempts_must_be_positive():
    with pytest.raises(ValueError):
        worker(max_attempts=0)


def test_clock_must_have_now():
    with pytest.raises(TypeError):
        ScheduledWorker(object())


def test_enqueue_at_returns_job_shape():
    job = worker().enqueue_at("email", {"to": "a@example.com"}, run_at=10)
    assert set(job) >= {"id", "job_type", "payload", "run_at", "timeout_seconds", "attempts", "status"}


def test_enqueue_assigns_incrementing_ids():
    w = worker()
    assert [w.enqueue_at("a", {}, 1)["id"], w.enqueue_at("b", {}, 1)["id"]] == [1, 2]


def test_enqueue_rejects_blank_job_type():
    with pytest.raises(ValueError):
        worker().enqueue_at(" ", {}, 1)


def test_enqueue_rejects_non_dict_payload():
    with pytest.raises(TypeError):
        worker().enqueue_at("email", [], 1)


def test_enqueue_in_uses_clock_delay():
    clock = FakeClock(100)
    w = ScheduledWorker(clock)
    assert w.enqueue_in("email", {}, 30)["run_at"] == 130


def test_enqueue_in_rejects_negative_delay():
    with pytest.raises(ValueError):
        worker().enqueue_in("email", {}, -1)


def test_timeout_must_be_positive():
    with pytest.raises(ValueError):
        worker().enqueue_at("email", {}, 1, timeout_seconds=0)


def test_run_due_does_not_run_future_jobs():
    clock = FakeClock(0)
    w = ScheduledWorker(clock)
    w.enqueue_at("email", {}, run_at=10)
    assert w.run_due({"email": lambda payload: "ok"}) == []


def test_run_due_runs_ready_job():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    w.enqueue_at("email", {"to": "a"}, run_at=10)
    assert w.run_due({"email": lambda payload: "sent"})[0]["status"] == "completed"


def test_run_due_runs_jobs_in_schedule_order():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    w.enqueue_at("second", {}, run_at=10)
    w.enqueue_at("first", {}, run_at=5)
    completed = w.run_due({"first": lambda p: "1", "second": lambda p: "2"})
    assert [job["job_type"] for job in completed] == ["first", "second"]


def test_fifo_for_same_run_at():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    w.enqueue_at("a", {}, run_at=10)
    w.enqueue_at("b", {}, run_at=10)
    completed = w.run_due({"a": lambda p: "a", "b": lambda p: "b"})
    assert [job["job_type"] for job in completed] == ["a", "b"]


def test_missing_handler_retries_job():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    job = w.enqueue_at("email", {}, run_at=10)
    result = w.run_due({})
    assert result[0]["status"] == "retry_scheduled"
    assert w.get_job(job["id"])["attempts"] == 1


def test_handler_exception_retries_until_max_attempts():
    clock = FakeClock(10)
    w = ScheduledWorker(clock, max_attempts=2)
    job = w.enqueue_at("email", {}, run_at=10)
    with pytest.raises(RuntimeError):
        w.run_due({"email": lambda payload: (_ for _ in ()).throw(RuntimeError("boom"))})
    assert w.get_job(job["id"])["status"] == "retry_scheduled"


def test_after_max_attempts_job_moves_to_dead_letters():
    clock = FakeClock(10)
    w = ScheduledWorker(clock, max_attempts=1)
    job = w.enqueue_at("email", {}, run_at=10)
    with pytest.raises(RuntimeError):
        w.run_due({"email": lambda payload: (_ for _ in ()).throw(RuntimeError("boom"))})
    assert w.dead_letters()[0]["id"] == job["id"]


def test_cancel_queued_job_returns_true():
    w = worker()
    job = w.enqueue_at("email", {}, run_at=10)
    assert w.cancel(job["id"]) is True


def test_cancelled_job_does_not_run():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    job = w.enqueue_at("email", {}, run_at=10)
    w.cancel(job["id"])
    assert w.run_due({"email": lambda payload: "sent"}) == []


def test_cancel_unknown_job_returns_false():
    assert worker().cancel(999) is False


def test_get_unknown_job_raises():
    with pytest.raises(KeyError):
        worker().get_job(999)


def test_payload_is_copied_on_enqueue():
    payload = {"to": "a"}
    job = worker().enqueue_at("email", payload, run_at=1)
    payload["to"] = "b"
    assert job["payload"] == {"to": "a"}


def test_dead_letters_returns_copy():
    clock = FakeClock(10)
    w = ScheduledWorker(clock, max_attempts=1)
    w.enqueue_at("email", {}, run_at=10)
    with pytest.raises(RuntimeError):
        w.run_due({"email": lambda payload: (_ for _ in ()).throw(RuntimeError("boom"))})
    letters = w.dead_letters()
    letters.clear()
    assert len(w.dead_letters()) == 1


def test_job_timeout_is_recorded():
    clock = FakeClock(10)
    w = ScheduledWorker(clock)
    w.enqueue_at("email", {}, run_at=10, timeout_seconds=1)
    with pytest.raises(JobTimeoutError):
        w.run_due({"email": lambda payload: (_ for _ in ()).throw(JobTimeoutError("timeout"))})
    assert w.dead_letters() == []
