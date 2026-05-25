class FixedWindowRateLimiter:
    def __init__(self, limit: int, window_seconds: int, clock):
        raise NotImplementedError
    def allow(self, user_id: str) -> bool:
        raise NotImplementedError

class TokenBucketRateLimiter:
    def __init__(self, limit: int, refill_seconds: int, clock):
        raise NotImplementedError
    def allow(self, user_id: str) -> bool:
        raise NotImplementedError
