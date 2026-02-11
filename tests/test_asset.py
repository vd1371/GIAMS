"""Unit tests for Asset types and elements."""

import numpy as np
import pytest
from Asset.AssetTypes.BaseAsset import BaseAsset
from Asset.Elements.BaseElement import BaseElement


def test_base_asset_set_elements_util_weight_equal(settings):
    """With weights=None, elements_util_weight is equal for n_elements."""
    asset = BaseAsset(ID=1, settings=settings)
    asset.elements = [None] * settings.n_elements  # placeholder
    asset.set_elements_util_weight()
    expected = 1.0 / settings.n_elements
    np.testing.assert_array_almost_equal(
        asset.elements_util_weight,
        np.array([expected] * settings.n_elements),
    )


def test_base_asset_set_elements_util_weight_custom(settings):
    """With list/array weights, elements_util_weight is set correctly."""
    asset = BaseAsset(ID=1, settings=settings)
    asset.elements = [None, None, None]
    w = [0.2, 0.3, 0.5]
    asset.set_elements_util_weight(weights=w)
    np.testing.assert_array_almost_equal(asset.elements_util_weight, np.array(w))


def test_base_asset_set_elements_util_weight_wrong_length_raises(settings):
    """Weights length must match number of elements."""
    asset = BaseAsset(ID=1, settings=settings)
    asset.elements = [None, None]
    with pytest.raises(ValueError, match="length of weights and elements"):
        asset.set_elements_util_weight(weights=[0.5, 0.5, 0.0])


def test_base_element_initial_age():
    """Element stores initial_age from params."""
    elem = BaseElement(age=5, name="Test")
    assert elem.age == 5
    assert elem.initial_age == 5


def test_base_element_refresh_age():
    """refresh_age resets age to initial_age."""
    elem = BaseElement(age=10, name="Test")
    elem.age = 20
    elem.refresh_age()
    assert elem.age == 10


def test_base_element_add_age():
    """add_age increments age by integer."""
    elem = BaseElement(age=0, name="Test")
    elem.add_age(3)
    assert elem.age == 3
    elem.add_age(2)
    assert elem.age == 5


def test_base_element_add_age_non_int_raises():
    """add_age with non-integer raises AssertionError."""
    elem = BaseElement(age=0, name="Test")
    with pytest.raises(AssertionError):
        elem.add_age(1.5)


def test_base_element_set_age():
    """set_age sets age to new value."""
    elem = BaseElement(age=5, name="Test")
    elem.set_age(7)
    assert elem.age == 7
