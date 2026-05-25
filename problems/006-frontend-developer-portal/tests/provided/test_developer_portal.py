from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from developer_portal import auth_headers, create_initial_state, fetch_all_pages, login, reducer, update_resource
class FakeAPI:
    def post(self,path,payload,headers=None): return {'token':'t'}
    def get(self,path,headers=None): return {'items':[],'next_page':None}
    def patch(self,path,payload,headers=None): return {'id':'r1', **payload}
def test_login_posts_credentials(): assert login(FakeAPI(),'a@example.com','pw')['token'] == 't'
def test_login_rejects_blank_email():
    with pytest.raises(ValueError): login(FakeAPI(),' ','pw')
def test_login_rejects_blank_password():
    with pytest.raises(ValueError): login(FakeAPI(),'a@example.com',' ')
def test_auth_headers_include_bearer_token(): assert auth_headers('abc') == {'Authorization':'Bearer abc'}
def test_auth_headers_reject_blank_token():
    with pytest.raises(ValueError): auth_headers(' ')
def test_initial_state_has_expected_keys(): assert set(create_initial_state()) >= {'token','loading','error','apps','resources','users'}
def test_reducer_login_started_sets_loading(): assert reducer(create_initial_state(), {'type':'login_started'})['loading'] is True
def test_reducer_login_succeeded_stores_token(): assert reducer(create_initial_state(), {'type':'login_succeeded','token':'t'})['token'] == 't'
def test_reducer_login_failed_stores_error(): assert reducer(create_initial_state(), {'type':'login_failed','error':'bad'})['error'] == 'bad'
def test_reducer_fetch_apps_succeeded_sets_apps(): assert reducer(create_initial_state(), {'type':'apps_loaded','apps':[{'id':'a'}]})['apps'] == [{'id':'a'}]
def test_reducer_resources_loaded_sets_resources(): assert reducer(create_initial_state(), {'type':'resources_loaded','resources':[{'id':'r'}]})['resources'] == [{'id':'r'}]
def test_reducer_users_loaded_sets_users(): assert reducer(create_initial_state(), {'type':'users_loaded','users':[{'id':'u'}]})['users'] == [{'id':'u'}]
def test_reducer_unknown_action_raises():
    with pytest.raises(ValueError): reducer(create_initial_state(), {'type':'wat'})
def test_reducer_does_not_mutate_input_state(): state=create_initial_state(); reducer(state, {'type':'login_started'}); assert state == create_initial_state()
def test_fetch_all_pages_returns_empty_items(): assert fetch_all_pages(FakeAPI(), '/apps') == []
def test_fetch_all_pages_follows_next_page():
    class API(FakeAPI):
        def __init__(self): self.n=0
        def get(self,path,headers=None): self.n+=1; return {'items':[{'id':self.n}], 'next_page':'/p2' if self.n==1 else None}
    assert [x['id'] for x in fetch_all_pages(API(), '/p1')] == [1,2]
def test_fetch_all_pages_preserves_order():
    class API(FakeAPI):
        def get(self,path,headers=None): return {'items':[{'id':'a'},{'id':'b'}], 'next_page':None}
    assert [x['id'] for x in fetch_all_pages(API(), '/p')] == ['a','b']
def test_fetch_all_pages_validates_shape():
    class API(FakeAPI):
        def get(self,path,headers=None): return {'data':[]}
    with pytest.raises(ValueError): fetch_all_pages(API(), '/p')
def test_update_resource_uses_patch_with_auth(): assert update_resource(FakeAPI(),'t','r1',{'name':'New'})['name'] == 'New'
def test_update_resource_rejects_empty_updates():
    with pytest.raises(ValueError): update_resource(FakeAPI(),'t','r1',{})
def test_update_resource_rejects_blank_id():
    with pytest.raises(ValueError): update_resource(FakeAPI(),'t',' ',{'name':'x'})
