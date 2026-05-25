from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from lru_cache import LRUCache
def test_capacity_must_be_positive():
    with pytest.raises(ValueError): LRUCache(0)
def test_negative_capacity_rejected():
    with pytest.raises(ValueError): LRUCache(-1)
def test_get_missing_returns_none(): assert LRUCache(1).get('x') is None
def test_put_then_get_returns_value(): c=LRUCache(1); c.put('a',1); assert c.get('a') == 1
def test_put_returns_none(): c=LRUCache(1); assert c.put('a',1) is None
def test_capacity_one_evicts_old_key(): c=LRUCache(1); c.put('a',1); c.put('b',2); assert c.get('a') is None
def test_capacity_one_keeps_new_key(): c=LRUCache(1); c.put('a',1); c.put('b',2); assert c.get('b') == 2
def test_least_recently_used_evicted(): c=LRUCache(2); c.put('a',1); c.put('b',2); c.put('c',3); assert c.get('a') is None
def test_get_refreshes_recency(): c=LRUCache(2); c.put('a',1); c.put('b',2); c.get('a'); c.put('c',3); assert c.get('b') is None
def test_update_existing_value(): c=LRUCache(2); c.put('a',1); c.put('a',9); assert c.get('a') == 9
def test_update_refreshes_recency(): c=LRUCache(2); c.put('a',1); c.put('b',2); c.put('a',9); c.put('c',3); assert c.get('b') is None
def test_none_value_can_be_stored(): c=LRUCache(1); c.put('a',None); assert c.get('a') is None
def test_false_value_can_be_stored(): c=LRUCache(1); c.put('a',False); assert c.get('a') is False
def test_zero_value_can_be_stored(): c=LRUCache(1); c.put('a',0); assert c.get('a') == 0
def test_string_keys_supported(): c=LRUCache(1); c.put('key','v'); assert c.get('key') == 'v'
def test_tuple_keys_supported(): c=LRUCache(1); c.put(('a',1),'v'); assert c.get(('a',1)) == 'v'
def test_multiple_gets_do_not_evict(): c=LRUCache(2); c.put('a',1); c.put('b',2); c.get('a'); c.get('a'); assert c.get('a') == 1
def test_eviction_after_refresh_chain(): c=LRUCache(3); c.put('a',1); c.put('b',2); c.put('c',3); c.get('a'); c.get('b'); c.put('d',4); assert c.get('c') is None
def test_get_missing_does_not_affect_recency(): c=LRUCache(2); c.put('a',1); c.put('b',2); c.get('x'); c.put('c',3); assert c.get('a') is None
def test_cache_handles_object_values_by_identity(): c=LRUCache(1); obj=[]; c.put('a',obj); assert c.get('a') is obj
