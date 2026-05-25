from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from message_board import MessageBoard
def user(b,n='alice'): return b.create_user(n)
def post(b,u,t='Hello'): return b.create_post(u['id'],t,'Body')
def test_create_user_assigns_id(): assert MessageBoard().create_user('alice')['id'] == 1
def test_create_user_rejects_blank_username():
    with pytest.raises(ValueError): MessageBoard().create_user(' ')
def test_duplicate_username_rejected():
    b=MessageBoard(); b.create_user('alice')
    with pytest.raises(ValueError): b.create_user('alice')

def test_create_post_assigns_id(): b=MessageBoard(); u=user(b); assert post(b,u)['id'] == 1
def test_create_post_requires_existing_user():
    with pytest.raises(KeyError): MessageBoard().create_post(99,'T','B')
def test_create_post_rejects_blank_title():
    b=MessageBoard(); u=user(b)
    with pytest.raises(ValueError): b.create_post(u['id'],' ','B')

def test_create_post_rejects_blank_body():
    b=MessageBoard(); u=user(b)
    with pytest.raises(ValueError): b.create_post(u['id'],'T',' ')

def test_list_posts_returns_newest_first(): b=MessageBoard(); u=user(b); b.create_post(u['id'],'First','B'); b.create_post(u['id'],'Second','B'); assert [p['title'] for p in b.list_posts()] == ['Second','First']
def test_list_posts_limit(): b=MessageBoard(); u=user(b); [b.create_post(u['id'],str(i),'B') for i in range(3)]; assert len(b.list_posts(limit=2)) == 2
def test_list_posts_offset(): b=MessageBoard(); u=user(b); [b.create_post(u['id'],str(i),'B') for i in range(3)]; assert len(b.list_posts(limit=2, offset=1)) == 2
def test_invalid_limit_rejected():
    with pytest.raises(ValueError): MessageBoard().list_posts(limit=0)
def test_invalid_offset_rejected():
    with pytest.raises(ValueError): MessageBoard().list_posts(offset=-1)
def test_add_comment_assigns_id(): b=MessageBoard(); u=user(b); p=post(b,u); assert b.add_comment(u['id'],p['id'],'Nice')['id'] == 1
def test_add_comment_requires_existing_user():
    b=MessageBoard(); u=user(b); p=post(b,u)
    with pytest.raises(KeyError): b.add_comment(99,p['id'],'X')

def test_add_comment_requires_existing_post():
    b=MessageBoard(); u=user(b)
    with pytest.raises(KeyError): b.add_comment(u['id'],99,'X')

def test_add_comment_rejects_blank_body():
    b=MessageBoard(); u=user(b); p=post(b,u)
    with pytest.raises(ValueError): b.add_comment(u['id'],p['id'],' ')

def test_delete_own_post_returns_true(): b=MessageBoard(); u=user(b); p=post(b,u); assert b.delete_post(u['id'],p['id']) is True
def test_delete_other_users_post_denied():
    b=MessageBoard(); a=user(b,'a'); c=user(b,'c'); p=post(b,a)
    with pytest.raises(PermissionError): b.delete_post(c['id'],p['id'])

def test_delete_own_comment_returns_true(): b=MessageBoard(); u=user(b); p=post(b,u); c=b.add_comment(u['id'],p['id'],'Nice'); assert b.delete_comment(u['id'],c['id']) is True
def test_delete_other_users_comment_denied():
    b=MessageBoard(); a=user(b,'a'); c=user(b,'c'); p=post(b,a); comment=b.add_comment(a['id'],p['id'],'Nice')
    with pytest.raises(PermissionError): b.delete_comment(c['id'],comment['id'])

def test_returned_posts_are_mutation_safe(): b=MessageBoard(); u=user(b); post(b,u); posts=b.list_posts(); posts[0]['title']='X'; assert b.list_posts()[0]['title'] == 'Hello'
