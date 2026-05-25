from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from buggy_order_processor import process_order, refund_order
def test_empty_order_total_zero(): assert process_order({'items':[]}, {})['total'] == 0
def test_single_item_subtotal(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}]}, {'a':1})['subtotal'] == 10
def test_tax_is_ten_percent(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}]}, {'a':1})['tax'] == 1
def test_total_includes_tax(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}]}, {'a':1})['total'] == 11
def test_fixed_discount_subtracts_amount(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}],'discount':2}, {'a':1})['subtotal'] == 8
def test_inventory_decrements_by_quantity(): inv={'a':5}; process_order({'items':[{'sku':'a','quantity':3,'unit_price':10}]}, inv); assert inv['a'] == 2
def test_out_of_stock_when_quantity_exceeds_inventory():
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':3,'unit_price':10}]}, {'a':2})
def test_missing_sku_out_of_stock():
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}]}, {})
def test_multiple_items_sum(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10},{'sku':'b','quantity':2,'unit_price':5}]}, {'a':1,'b':2})['subtotal'] == 20
def test_refund_restores_quantity(): inv={'a':0}; refund_order({'items':[{'sku':'a','quantity':3,'unit_price':10}]}, inv); assert inv['a'] == 3
def test_refund_returns_true(): assert refund_order({'items':[]}, {}) is True
def test_percentage_discount_supported(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':100}],'discount':{'type':'percent','value':10}}, {'a':1})['subtotal'] == 90
def test_discount_cannot_make_subtotal_negative(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':10}],'discount':20}, {'a':1})['subtotal'] == 0
def test_rejects_negative_quantity():
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':-1,'unit_price':10}]}, {'a':1})
def test_rejects_zero_quantity():
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':0,'unit_price':10}]}, {'a':1})
def test_rejects_negative_price():
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':1,'unit_price':-1}]}, {'a':1})
def test_rounds_money_to_two_decimals(): assert process_order({'items':[{'sku':'a','quantity':1,'unit_price':0.1}]}, {'a':1})['total'] == 0.11
def test_inventory_unchanged_when_order_fails():
    inv={'a':1,'b':0}
    with pytest.raises(ValueError): process_order({'items':[{'sku':'a','quantity':1,'unit_price':10},{'sku':'b','quantity':1,'unit_price':10}]}, inv)
    assert inv == {'a':1,'b':0}
def test_missing_items_key_is_rejected():
    with pytest.raises(ValueError): process_order({}, {})
def test_refund_rejects_unknown_sku():
    with pytest.raises(KeyError): refund_order({'items':[{'sku':'x','quantity':1}]}, {})
