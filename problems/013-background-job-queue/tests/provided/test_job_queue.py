from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from job_queue import JobQueue
def test_max_attempts_positive():
    with pytest.raises(ValueError): JobQueue(max_attempts=0)
def test_enqueue_assigns_id(): assert JobQueue().enqueue('email',{})['id'] == 1
def test_enqueue_sets_status_queued(): assert JobQueue().enqueue('email',{})['status'] == 'queued'
def test_enqueue_preserves_payload(): assert JobQueue().enqueue('email',{'x':1})['payload'] == {'x':1}
def test_enqueue_rejects_blank_type():
    with pytest.raises(ValueError): JobQueue().enqueue(' ',{})
def test_enqueue_rejects_non_dict_payload():
    with pytest.raises(TypeError): JobQueue().enqueue('email',[])
def test_reserve_next_returns_none_when_empty(): assert JobQueue().reserve_next() is None
def test_reserve_next_fifo(): q=JobQueue(); q.enqueue('a',{}); q.enqueue('b',{}); assert [q.reserve_next()['job_type'],q.reserve_next()['job_type']] == ['a','b']
def test_reserved_job_status_running(): q=JobQueue(); q.enqueue('a',{}); assert q.reserve_next()['status'] == 'running'
def test_complete_running_job(): q=JobQueue(); job=q.enqueue('a',{}); q.reserve_next(); assert q.complete(job['id']) is None
def test_complete_unknown_job_fails():
    with pytest.raises(KeyError): JobQueue().complete(99)
def test_cannot_complete_same_job_twice():
    q=JobQueue(); job=q.enqueue('a',{}); q.reserve_next(); q.complete(job['id'])
    with pytest.raises(ValueError): q.complete(job['id'])
def test_fail_requeues_until_max_attempts(): q=JobQueue(max_attempts=2); job=q.enqueue('a',{}); q.reserve_next(); q.fail(job['id'],'boom'); assert q.reserve_next()['id'] == job['id']
def test_fail_after_max_attempts_dead_letters(): q=JobQueue(max_attempts=1); job=q.enqueue('a',{}); q.reserve_next(); q.fail(job['id'],'boom'); assert q.reserve_next() is None
def test_dead_letter_contains_failed_job(): q=JobQueue(max_attempts=1); job=q.enqueue('a',{}); q.reserve_next(); q.fail(job['id'],'boom'); assert q.dead_letters()[0]['id'] == job['id']
def test_fail_unknown_job_fails():
    with pytest.raises(KeyError): JobQueue().fail(99,'boom')
@pytest.mark.parametrize('reason', ['', ' '])
def test_blank_fail_reason_rejected(reason):
    q=JobQueue(); job=q.enqueue('a',{}); q.reserve_next()
    with pytest.raises(ValueError): q.fail(job['id'], reason)
def test_payload_mutation_safe_on_enqueue(): q=JobQueue(); payload={'x':1}; job=q.enqueue('a',payload); payload['x']=2; assert job['payload'] == {'x':1}
def test_reserved_payload_preserved(): q=JobQueue(); q.enqueue('a',{'x':1}); assert q.reserve_next()['payload'] == {'x':1}
def test_dead_letters_returns_copy(): q=JobQueue(max_attempts=1); job=q.enqueue('a',{}); q.reserve_next(); q.fail(job['id'],'boom'); letters=q.dead_letters(); letters.clear(); assert len(q.dead_letters()) == 1
def test_attempt_count_increments_on_reserve(): q=JobQueue(); q.enqueue('a',{}); assert q.reserve_next()['attempts'] == 1
