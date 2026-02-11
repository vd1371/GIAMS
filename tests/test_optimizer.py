"""Unit tests for Optimizer (objectives/solutions)."""

import numpy as np
import pytest
from Optimizer._objectives import BaseSolution, DeJong, num_hash, binary_to_num, num_to_binary


def test_binary_to_num():
    """binary_to_num converts binary array to number (scaled by 100)."""
    arr = np.array([1, 0, 1, 1])  # binary 1011 -> int 11, then /100 -> 0.11
    out = binary_to_num(arr)
    assert out == 0.11


def test_num_to_binary_roundtrip():
    """num_to_binary and binary_to_num are consistent for values in range."""
    shape = (1, 2, 10)  # 10 bits enough for 2 decimal * 100
    num = 2.55  # 255 fits in 8+ bits
    binary = num_to_binary(num, shape)
    back = binary_to_num(binary)
    assert abs(back - num) < 0.02  # 2 decimal places in encoding


def test_num_hash_array():
    """num_hash returns a string for 3D solution array (n_assets, n_elements, n_bits)."""
    # Shape: 1 asset, 2 elements, 4 bits each
    arr = np.array([[[1, 0, 1, 0], [0, 1, 0, 1]]])
    h = num_hash(arr)
    assert isinstance(h, str)
    assert "-" in h or len(h) >= 1


def test_base_solution_with_solut():
    """BaseSolution with solut param (3D MRR-style) sets shape from array."""
    # LCASolution uses (n_assets, n_elements, n_steps) with 0/1
    solut = np.array([[[1, 0, 1], [0, 1, 0]]])  # 1 asset, 2 elements, 3 steps
    sol = BaseSolution(solut=solut, val=42.0)
    assert sol.value == 42.0
    assert np.shape(sol.get_solut()) == (1, 2, 3)


def test_base_solution_with_shape():
    """BaseSolution with shape param (no solut) sets hash_ to None."""
    sol = BaseSolution(shape=(1, 2, 5))
    assert sol.hash_ is None
    assert sol.shape == (1, 2, 5)


def test_de_jong_evaluate_valid():
    """DeJong evaluate sets value for valid solution."""
    np.random.seed(0)
    sol = DeJong(shape=(1, 4, 10))  # validation_dimension=4, 10 bits per dim
    sol.random_init()
    sol.evaluate()
    assert sol.value != -np.inf
    assert sol.value <= 0
