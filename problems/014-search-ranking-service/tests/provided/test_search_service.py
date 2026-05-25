from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from search_service import SearchService
def seeded(): s=SearchService(); s.add_document('1','Python Guide','Learn testing',['python']); s.add_document('2','Testing','Python pytest tips',['python','testing']); return s
def test_add_document_returns_none(): assert SearchService().add_document('1','T','B') is None
def test_search_finds_title_case_insensitive(): assert seeded().search('python')[0]['doc_id'] == '1'
def test_search_finds_body_case_insensitive(): assert any(r['doc_id'] == '2' for r in seeded().search('PYTEST'))
def test_title_matches_rank_above_body_matches(): assert seeded().search('python')[0]['doc_id'] == '1'
def test_more_term_matches_rank_higher(): s=SearchService(); s.add_document('1','alpha beta','',[]); s.add_document('2','alpha','',[]); assert s.search('alpha beta')[0]['doc_id'] == '1'
def test_stable_tie_break_by_insertion_order(): s=SearchService(); s.add_document('1','alpha','',[]); s.add_document('2','alpha','',[]); assert [r['doc_id'] for r in s.search('alpha')] == ['1','2']
def test_tag_filter_limits_results(): assert [r['doc_id'] for r in seeded().search('python', tags=['testing'])] == ['2']
def test_multiple_tags_require_all_tags(): assert [r['doc_id'] for r in seeded().search('python', tags=['python','testing'])] == ['2']
def test_limit_applies(): assert len(seeded().search('python', limit=1)) == 1
def test_offset_applies(): assert len(seeded().search('python', offset=1)) == 1
def test_invalid_limit_rejected():
    with pytest.raises(ValueError): SearchService().search('x', limit=0)
def test_invalid_offset_rejected():
    with pytest.raises(ValueError): SearchService().search('x', offset=-1)
def test_empty_query_returns_empty_list(): assert SearchService().search('') == []
def test_blank_query_returns_empty_list(): assert SearchService().search('   ') == []
def test_duplicate_doc_id_updates_document(): s=SearchService(); s.add_document('1','old','',[]); s.add_document('1','new','',[]); assert s.search('old') == [] and s.search('new')[0]['doc_id'] == '1'
def test_add_document_rejects_blank_id():
    with pytest.raises(ValueError): SearchService().add_document(' ','T','B')
def test_add_document_rejects_blank_title_and_body():
    with pytest.raises(ValueError): SearchService().add_document('1',' ',' ')
def test_tags_default_to_empty(): s=SearchService(); s.add_document('1','T','body'); assert s.search('body')
def test_search_result_contains_score(): assert 'score' in seeded().search('python')[0]
def test_search_result_contains_title(): assert 'title' in seeded().search('python')[0]
def test_results_are_mutation_safe(): s=seeded(); r=s.search('python'); r[0]['title']='X'; assert s.search('python')[0]['title'] != 'X'
