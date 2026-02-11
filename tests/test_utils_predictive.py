"""Unit tests for utils.PredictiveModels.Linear."""

import numpy as np
import pytest
from utils.PredictiveModels.Linear import Linear


def test_linear_predict(settings):
    """Linear.predict(t) = drift * t + X0."""
    m = Linear(X0=100.0, drift=5.0, settings=settings)
    assert m.predict(t=0) == 100.0
    assert m.predict(t=2) == 110.0


def test_linear_predict_series_shape(settings):
    """predict_series returns array of length n_steps."""
    m = Linear(X0=0.0, drift=1.0, settings=settings)
    series = m.predict_series(random=True)
    assert len(series) == settings.n_steps
    assert isinstance(series, np.ndarray)


def test_linear_predict_series_deterministic(settings):
    """predict_series(random=False) returns stored series."""
    m = Linear(X0=10.0, drift=0.5, settings=settings)
    first = m.predict_series(random=True)
    second = m.predict_series(random=False)
    np.testing.assert_array_almost_equal(first, second)
