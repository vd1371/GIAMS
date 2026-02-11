"""Unit tests for LifeCycleAnalyzer."""

import pytest
from LifeCycleAnalyzer.BaseLCA import BaseLCA
from tests.conftest import SimpleSettings


def test_base_lca_requires_settings():
    """BaseLCA requires 'settings' in params."""
    with pytest.raises(KeyError):
        BaseLCA(lca_name="Test")


def test_base_lca_init(settings):
    """BaseLCA accepts settings and optional params."""
    lca = BaseLCA(settings=settings, lca_name="TestLCA")
    assert lca.settings is settings
    assert lca.lca_name == "TestLCA"
    assert lca.network is None
    assert lca.simulator is None


def test_base_lca_default_name(settings):
    """Default lca_name is 'Unknown'."""
    lca = BaseLCA(settings=settings)
    assert lca.lca_name == "Unknown"
