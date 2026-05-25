from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from task_service import TaskService
def test_create_task_assigns_id_one(): assert TaskService().create_task('Buy milk')['id'] == 1
def test_create_task_defaults_status_todo(): assert TaskService().create_task('A')['status'] == 'todo'
def test_create_task_keeps_description(): assert TaskService().create_task('A','B')['description'] == 'B'
def test_ids_auto_increment(): s=TaskService(); assert [s.create_task('A')['id'],s.create_task('B')['id']] == [1,2]
def test_title_is_required():
    with pytest.raises(ValueError): TaskService().create_task('')
def test_blank_title_is_rejected():
    with pytest.raises(ValueError): TaskService().create_task('   ')
def test_invalid_status_on_create_is_rejected():
    with pytest.raises(ValueError): TaskService().create_task('A', status='blocked')
def test_get_task_returns_created_task(): s=TaskService(); t=s.create_task('A'); assert s.get_task(t['id'])['title'] == 'A'
def test_get_unknown_task_fails_clearly():
    with pytest.raises(KeyError): TaskService().get_task(999)
def test_list_tasks_returns_creation_order(): s=TaskService(); s.create_task('A'); s.create_task('B'); assert [t['title'] for t in s.list_tasks()] == ['A','B']
def test_list_tasks_filters_by_status(): s=TaskService(); s.create_task('A'); s.create_task('B', status='done'); assert [t['title'] for t in s.list_tasks('done')] == ['B']
def test_invalid_filter_status_is_rejected():
    with pytest.raises(ValueError): TaskService().list_tasks('later')
def test_update_title_changes_task(): s=TaskService(); t=s.create_task('A'); assert s.update_task(t['id'], title='B')['title'] == 'B'
def test_update_status_changes_task(): s=TaskService(); t=s.create_task('A'); assert s.update_task(t['id'], status='done')['status'] == 'done'
def test_update_description_changes_task(): s=TaskService(); t=s.create_task('A'); assert s.update_task(t['id'], description='D')['description'] == 'D'
def test_update_unknown_field_fails():
    s=TaskService(); t=s.create_task('A')
    with pytest.raises(ValueError): s.update_task(t['id'], owner='me')
def test_update_unknown_task_fails():
    with pytest.raises(KeyError): TaskService().update_task(99, title='B')
def test_delete_existing_task_returns_true(): s=TaskService(); t=s.create_task('A'); assert s.delete_task(t['id']) is True
def test_delete_removes_task(): s=TaskService(); t=s.create_task('A'); s.delete_task(t['id']); assert s.list_tasks() == []
def test_delete_unknown_task_returns_false(): assert TaskService().delete_task(404) is False
def test_returned_task_mutation_does_not_change_internal_state(): s=TaskService(); t=s.create_task('A'); t['title']='X'; assert s.get_task(1)['title'] == 'A'
def test_timestamps_are_present(): t=TaskService().create_task('A'); assert t['created_at'] and t['updated_at']
