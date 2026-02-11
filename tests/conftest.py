"""Pytest fixtures for GIAMS tests."""

import pytest


class SimpleSettings:
    """Minimal settings object for tests (matches GeneralSettings usage)."""

    n_elements = 3
    n_states = 8
    dt = 2
    horizon = 20
    discount_rate = 0.03
    init_year = 0
    n_steps = 10  # horizon / dt


@pytest.fixture
def settings():
    return SimpleSettings()
