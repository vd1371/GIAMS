"""Unit tests for utils.NPV."""

import pytest
from utils.NPV import NPV


def test_npv_zero_discount():
    """NPV with r=0 is sum of cash flows."""
    costs = [10.0, 20.0, 30.0]
    assert NPV(costs, dt=1, r=0) == 60.0


def test_npv_single_value():
    """Single value at t=0 equals that value."""
    costs = [100.0]
    assert NPV(costs, dt=1, r=0.05) == 100.0


def test_npv_discounting():
    """NPV with positive discount rate reduces later values."""
    costs = [0.0, 0.0, 100.0]
    dt = 1
    r = 0.1
    val = NPV(costs, dt, r)
    # 100 * exp(-0.1*2) ≈ 81.87
    assert 80 < val < 83


def test_npv_dt_affects_exponent():
    """Larger dt increases discounting over same number of steps."""
    costs = [0.0, 0.0, 100.0]
    val_dt1 = NPV(costs, dt=1, r=0.1)
    val_dt2 = NPV(costs, dt=2, r=0.1)
    assert val_dt2 < val_dt1
