from pathlib import Path
import asyncio
import sys

import pytest

PROBLEM_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROBLEM_ROOT / "src"))

from async_task_runner import run_tasks


def run(coro):
    return asyncio.run(coro)


async def value(x):
    return x


def make_task(x):
    return lambda: value(x)


def test_empty_tasks_returns_empty_list():
    assert run(run_tasks([], 1)) == []


def test_limit_must_be_positive():
    with pytest.raises(ValueError):
        run(run_tasks([make_task(1)], 0))


def test_runs_single_task():
    assert run(run_tasks([make_task(1)], 1)) == [1]


def test_preserves_order():
    assert run(run_tasks([make_task(2), make_task(1)], 2)) == [2, 1]


def test_runs_all_tasks():
    assert run(run_tasks([make_task(i) for i in range(5)], 2)) == list(range(5))


def test_concurrency_limit_one_runs_sequentially():
    active = 0
    max_active = 0

    async def job():
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0)
        active -= 1
        return max_active

    run(run_tasks([lambda: job(), lambda: job()], 1))
    assert max_active == 1


def test_concurrency_limit_two_allows_two():
    active = 0
    max_active = 0

    async def job():
        nonlocal active, max_active
        active += 1
        max_active = max(max_active, active)
        await asyncio.sleep(0)
        active -= 1
        return max_active

    run(run_tasks([lambda: job(), lambda: job(), lambda: job()], 2))
    assert max_active <= 2


def test_failure_is_captured_clearly():
    async def bad():
        raise RuntimeError("boom")

    result = run(run_tasks([lambda: bad()], 1))
    assert "boom" in str(result[0])


def test_mixed_success_and_failure_preserves_slots():
    async def bad():
        raise RuntimeError("boom")

    result = run(run_tasks([make_task("ok"), lambda: bad()], 2))
    assert result[0] == "ok"
    assert "boom" in str(result[1])


def test_tasks_are_callables():
    with pytest.raises(TypeError):
        run(run_tasks([object()], 1))


def test_task_must_return_awaitable():
    with pytest.raises(TypeError):
        run(run_tasks([lambda: 1], 1))


def test_limit_greater_than_task_count_ok():
    assert run(run_tasks([make_task(1)], 10)) == [1]


def test_negative_limit_rejected():
    with pytest.raises(ValueError):
        run(run_tasks([], -1))


def test_none_tasks_rejected():
    with pytest.raises(TypeError):
        run(run_tasks(None, 1))


def test_does_not_mutate_task_list():
    tasks = [make_task(1)]
    run(run_tasks(tasks, 1))
    assert len(tasks) == 1


def test_accepts_tuple_tasks():
    assert run(run_tasks((make_task(1),), 1)) == [1]


def test_many_tasks_with_small_limit():
    assert run(run_tasks([make_task(i) for i in range(20)], 3)) == list(range(20))


def test_return_type_is_list():
    assert isinstance(run(run_tasks([], 1)), list)


def test_synchronous_exception_from_factory_captured():
    def bad():
        raise RuntimeError("factory")

    result = run(run_tasks([bad], 1))
    assert "factory" in str(result[0])


def test_cancelled_error_is_reported():
    async def bad():
        raise asyncio.CancelledError()

    result = run(run_tasks([lambda: bad()], 1))
    assert "cancel" in str(result[0]).lower()
