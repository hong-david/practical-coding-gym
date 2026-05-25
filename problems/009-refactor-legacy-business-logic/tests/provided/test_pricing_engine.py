from pathlib import Path
import sys, pytest
PROBLEM_ROOT=Path(__file__).resolve().parents[2]; sys.path.insert(0,str(PROBLEM_ROOT/'src'))
from pricing_engine import calculate_price
def test_free_plan_zero(): assert calculate_price('free',1) == 0
def test_starter_base_price(): assert calculate_price('starter',1) == 19
def test_pro_base_price(): assert calculate_price('pro',1) == 49
def test_enterprise_base_price(): assert calculate_price('enterprise',1) == 199
def test_unknown_plan_rejected():
    with pytest.raises(ValueError): calculate_price('bogus',1)
def test_extra_users_add_five_each_starter(): assert calculate_price('starter',3) == 29
def test_extra_users_add_five_each_pro(): assert calculate_price('pro',4) == 64
def test_free_plan_ignores_extra_users(): assert calculate_price('free',10) == 0
def test_save10_coupon(): assert calculate_price('starter',1,'SAVE10') == 17.1
def test_half_coupon(): assert calculate_price('pro',1,'HALF') == 24.5
def test_unknown_coupon_ignored_for_legacy_behavior(): assert calculate_price('starter',1,'NOPE') == 19
def test_pro_renewal_discount(): assert calculate_price('pro',1,renewing=True) == 46.55
def test_enterprise_renewal_discount(): assert calculate_price('enterprise',1,renewing=True) == 189.05
def test_starter_no_renewal_discount(): assert calculate_price('starter',1,renewing=True) == 19
def test_coupon_then_renewal_order_existing_behavior(): assert calculate_price('pro',1,'SAVE10',True) == 41.9
def test_rounds_to_two_decimals(): assert calculate_price('starter',2,'SAVE10') == 21.6
def test_zero_users_rejected_new_feature():
    with pytest.raises(ValueError): calculate_price('starter',0)
def test_negative_users_rejected_new_feature():
    with pytest.raises(ValueError): calculate_price('starter',-1)
def test_annual_coupon_todo_new_feature(): assert calculate_price('starter',1,'ANNUAL20') == 15.2
def test_plan_names_are_case_sensitive_existing_behavior():
    with pytest.raises(ValueError): calculate_price('Starter',1)
