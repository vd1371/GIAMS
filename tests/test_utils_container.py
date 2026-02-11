"""Unit tests for utils.Container."""

import numpy as np
import pytest
from utils.Container import Container


def test_container_update_stepwise(settings):
    """stepwise average updates correctly."""
    c = Container(settings=settings)
    assert c.simulator_counter == 0
    c.update_stepwise(np.ones(settings.n_steps))
    assert c.simulator_counter == 1
    np.testing.assert_array_almost_equal(c.get_stepwise(), np.ones(settings.n_steps))
    c.update_stepwise(np.ones(settings.n_steps) * 3)
    assert c.simulator_counter == 2
    # average of [1,1,...] and [3,3,...] is [2,2,...]
    np.testing.assert_array_almost_equal(c.get_stepwise(), np.ones(settings.n_steps) * 2)


def test_container_add_npv_samples(settings):
    """add_to_npv_samples appends and get_samples returns them."""
    c = Container(settings=settings)
    c.add_to_npv_samples(10.0)
    c.add_to_npv_samples(20.0)
    assert c.get_samples() == [10.0, 20.0]


def test_container_expected(settings):
    """expected() returns (mean, std) of NPV samples."""
    c = Container(settings=settings)
    c.add_to_npv_samples(10.0)
    c.add_to_npv_samples(20.0)
    mean, std = c.expected()
    assert mean == 15.0
    assert std == round(5.0, 2)  # sqrt(50) ≈ 7.07, rounded to 2 decimals


def test_container_at_year(settings):
    """at_year returns stepwise value at given step index."""
    c = Container(settings=settings)
    arr = np.arange(settings.n_steps, dtype=float)
    c.update_stepwise(arr)
    # year 0 -> index 0, year 2 with dt=2 -> index 1
    assert c.at_year(0) == 0.0
    assert c.at_year(2) == 1.0
