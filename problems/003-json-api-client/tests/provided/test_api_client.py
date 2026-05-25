from pathlib import Path
import sys
import pytest
PROBLEM_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROBLEM_ROOT / "src"))
from api_client import APIClient, APIClientError, BadResponseError, PermanentAPIError, TransientAPIError
class FakeTransport:
    def __init__(self, responses): self.responses=list(responses); self.calls=[]
    def get(self, endpoint):
        self.calls.append(endpoint); response=self.responses.pop(0)
        if isinstance(response, Exception): raise response
        return response

def test_fetch_all_items_single_page(): assert APIClient(FakeTransport([{"items":[{"id":"1"}],"next_page":None}])).fetch_all_items("/items") == [{"id":"1"}]
def test_fetch_all_items_multiple_pages_preserves_order(): assert APIClient(FakeTransport([{"items":[{"id":"1"}],"next_page":"/p2"},{"items":[{"id":"2"}],"next_page":None}])).fetch_all_items("/p1") == [{"id":"1"},{"id":"2"}]
def test_fetches_next_page_url():
    t=FakeTransport([{"items":[],"next_page":"/p2"},{"items":[],"next_page":None}]); APIClient(t).fetch_all_items("/p1"); assert t.calls == ["/p1","/p2"]
def test_empty_page_returns_empty_list(): assert APIClient(FakeTransport([{"items":[],"next_page":None}])).fetch_all_items("/items") == []
def test_empty_middle_page_continues(): assert APIClient(FakeTransport([{"items":[],"next_page":"/p2"},{"items":[{"id":"2"}],"next_page":None}])).fetch_all_items("/p1") == [{"id":"2"}]
def test_duplicate_ids_preserve_raw_order(): assert APIClient(FakeTransport([{"items":[{"id":"1"},{"id":"1"}],"next_page":None}])).fetch_all_items("/items") == [{"id":"1"},{"id":"1"}]
def test_response_objects_are_not_mutated():
    r={"items":[{"id":"1"}],"next_page":None}; APIClient(FakeTransport([r])).fetch_all_items("/items"); assert r == {"items":[{"id":"1"}],"next_page":None}
def test_retries_transient_errors():
    t=FakeTransport([TransientAPIError("boom"),{"items":[],"next_page":None}]); APIClient(t,max_retries=1).fetch_all_items("/items"); assert len(t.calls) == 2
def test_exhausted_retries_raise_client_error():
    with pytest.raises(APIClientError): APIClient(FakeTransport([TransientAPIError("a"),TransientAPIError("b")]),max_retries=1).fetch_all_items("/items")
def test_does_not_retry_permanent_errors():
    t=FakeTransport([PermanentAPIError("bad")])
    with pytest.raises(PermanentAPIError): APIClient(t).fetch_all_items("/items")
    assert len(t.calls) == 1
def test_429_rate_limit_is_retried():
    t=FakeTransport([APIClientError("429"),{"items":[],"next_page":None}]); APIClient(t,max_retries=1).fetch_all_items("/items"); assert len(t.calls)==2
def test_missing_items_key_is_bad_response():
    with pytest.raises(BadResponseError): APIClient(FakeTransport([{"next_page":None}])).fetch_all_items("/items")
def test_items_must_be_list():
    with pytest.raises(BadResponseError): APIClient(FakeTransport([{"items":{},"next_page":None}])).fetch_all_items("/items")
def test_next_page_key_is_required():
    with pytest.raises(BadResponseError): APIClient(FakeTransport([{"items":[]}])).fetch_all_items("/items")
def test_next_page_may_be_none_or_string_only():
    with pytest.raises(BadResponseError): APIClient(FakeTransport([{"items":[],"next_page":2}])).fetch_all_items("/items")
def test_fetch_item_returns_matching_item(): assert APIClient(FakeTransport([{"items":[{"id":"a"}],"next_page":None}])).fetch_item("/items","a") == {"id":"a"}
def test_fetch_item_searches_later_pages(): assert APIClient(FakeTransport([{"items":[{"id":"a"}],"next_page":"/p2"},{"items":[{"id":"b"}],"next_page":None}])).fetch_item("/items","b") == {"id":"b"}
def test_fetch_item_missing_raises_clear_error():
    with pytest.raises(APIClientError, match="missing"): APIClient(FakeTransport([{"items":[],"next_page":None}])).fetch_item("/items","missing")
def test_max_retries_cannot_be_negative():
    with pytest.raises(ValueError): APIClient(FakeTransport([]), max_retries=-1)
def test_transport_must_provide_get():
    with pytest.raises(TypeError): APIClient(object())
