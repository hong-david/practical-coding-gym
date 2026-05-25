from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from rate_limiter import FixedWindowRateLimiter
class Clock:
    def __init__(self,t=0): self.t=t
    def now(self): return self.t
    def advance(self,s): self.t += s
def test_limit_must_be_positive():
    with pytest.raises(ValueError): FixedWindowRateLimiter(0,60,Clock())
def test_window_must_be_positive():
    with pytest.raises(ValueError): FixedWindowRateLimiter(1,0,Clock())
def test_allows_first_request(): assert FixedWindowRateLimiter(1,60,Clock()).allow('u') is True
def test_blocks_after_limit(): r=FixedWindowRateLimiter(1,60,Clock()); r.allow('u'); assert r.allow('u') is False
def test_allows_exactly_limit_requests(): r=FixedWindowRateLimiter(2,60,Clock()); assert [r.allow('u'),r.allow('u')] == [True,True]
def test_resets_after_window(): c=Clock(); r=FixedWindowRateLimiter(1,60,c); r.allow('u'); c.advance(60); assert r.allow('u') is True
def test_does_not_reset_before_window(): c=Clock(); r=FixedWindowRateLimiter(1,60,c); r.allow('u'); c.advance(59); assert r.allow('u') is False
def test_boundary_at_window_start_resets(): c=Clock(120); r=FixedWindowRateLimiter(1,60,c); r.allow('u'); c.advance(60); assert r.allow('u') is True
def test_users_are_independent(): r=FixedWindowRateLimiter(1,60,Clock()); r.allow('a'); assert r.allow('b') is True
def test_blocked_user_does_not_block_other_user(): r=FixedWindowRateLimiter(1,60,Clock()); r.allow('a'); r.allow('a'); assert r.allow('b') is True
def test_blank_user_rejected():
    with pytest.raises(ValueError): FixedWindowRateLimiter(1,60,Clock()).allow(' ')
def test_multiple_windows_count_independently(): c=Clock(); r=FixedWindowRateLimiter(2,10,c); r.allow('u'); r.allow('u'); c.advance(10); assert [r.allow('u'),r.allow('u'),r.allow('u')] == [True,True,False]
def test_clock_object_must_have_now():
    with pytest.raises(TypeError): FixedWindowRateLimiter(1,60,object())
def test_string_user_ids_supported(): assert FixedWindowRateLimiter(1,60,Clock()).allow('user-1') is True
def test_counts_within_same_window(): r=FixedWindowRateLimiter(3,60,Clock()); assert [r.allow('u') for _ in range(4)] == [True,True,True,False]
def test_new_user_starts_fresh_late_in_window(): c=Clock(59); r=FixedWindowRateLimiter(1,60,c); assert r.allow('u') is True
def test_window_calculated_from_epoch_boundaries(): c=Clock(59); r=FixedWindowRateLimiter(1,60,c); r.allow('u'); c.advance(1); assert r.allow('u') is True
def test_large_time_jump_resets(): c=Clock(); r=FixedWindowRateLimiter(1,60,c); r.allow('u'); c.advance(1000); assert r.allow('u') is True
def test_repeated_blocked_calls_stay_blocked(): r=FixedWindowRateLimiter(1,60,Clock()); r.allow('u'); assert [r.allow('u'),r.allow('u')] == [False,False]
def test_return_type_is_bool(): assert isinstance(FixedWindowRateLimiter(1,60,Clock()).allow('u'), bool)
