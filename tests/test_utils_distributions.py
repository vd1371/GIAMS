"""Unit tests for utils.Distributions."""

import numpy as np
import pytest
from utils.Distributions.Normal import Normal


def test_normal_sample_shape():
    """Normal.sample() returns a scalar."""
    d = Normal(0.0, 1.0)
    s = d.sample()
    assert np.isscalar(s) or (isinstance(s, (int, float)))


def test_normal_sample_mean_variance():
    """Sample mean and variance approximate mu and sigma^2."""
    np.random.seed(42)
    d = Normal(5.0, 2.0)
    # Use the generator that Normal uses
    samples = [d.sample() for _ in range(5000)]
    mean = np.mean(samples)
    var = np.var(samples)
    assert 4.7 < mean < 5.3
    assert 3.5 < var < 4.5


def test_normal_set():
    """set() updates mu and sigma."""
    d = Normal(0.0, 1.0)
    d.set(10.0, 3.0)
    assert d.mu == 10.0
    assert d.sigma == 3.0
