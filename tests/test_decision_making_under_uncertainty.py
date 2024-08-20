import pytest
import numpy as np
from src.decision_making_under_uncertainty import DecisionMakingUnderUncertainty
from contextlib import nullcontext as does_not_raise

@pytest.fixture
def default_matrix():
    return np.array([
    [3200, 4500, 5100, 3300],
    [4900, 3100, 5300, 4700],
    [3400, 5200, 3600, 5400],
    [4000, 3500, 5350, 3700],
    [3000, 4600, 5000, 3800]
])

@pytest.fixture
def big_matrix():
    return np.array([
    [10200, 8700, 7200, 14400, 8200, 9300, 13400],
    [9200, 10600, 8700, 15000, 7300, 11200, 8900],
    [9800, 10100, 10900, 8000, 12800, 9200, 7200],
    [14000, 8900, 7600, 14300, 8500, 11300, 9600],
    [8100, 10200, 14700, 9200, 9800, 13900, 8600],
    [11400, 7200, 13100, 9800, 10700, 14200, 7700],
    [7500, 14600, 8600, 11000, 8900, 13900, 9200]
])

@pytest.fixture
def single_element_matrix():
    return np.array([1])

@pytest.fixture
def multiple_optimal_strategies_matrix():
    return np.array([
        [2200, 3000, 3900],
        [1600, 2800, 4300],
        [2000, 3400, 3600],
        [1800, 2900, 3850],
        [1700, 3500, 3900],
        [1600, 3000, 4100], 
        [1000, 2700, 4000]
    ])

@pytest.fixture
def equal_rows_and_solutions_matrix():
    return np.array([
        [4100, 4500, 3900, 4800],
        [3700, 4100, 4300, 3600],
        [4100, 4500, 3900, 4800],
        [3850, 4200, 4100, 4500],
        [3600, 3900, 3700, 4600]
    ])

@pytest.fixture
def empty_matrix():
    return np.array([])

class TestDecisionMakingUnderUncertainty():
    @pytest.mark.parametrize(
        "matrix, res, expectation",
        [
            ("default_matrix", 4, does_not_raise()),
            ("big_matrix", 5, does_not_raise()),
            ("single_element_matrix", 1, does_not_raise()),
            ("multiple_optimal_strategies_matrix", 1, does_not_raise()),
            ("equal_rows_and_solutions_matrix", [1,3], does_not_raise()),
            ("empty_matrix", None, pytest.raises(ValueError))
        ]
    )
    def test_wald_criterion(self, matrix, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderUncertainty.wald_criterion(matrix) == res

    @pytest.mark.parametrize(
        "matrix, res, expectation",
        [
            ("default_matrix", 2, does_not_raise()),
            ("big_matrix", 5, does_not_raise()),
            ("single_element_matrix", 1, does_not_raise()),
            ("multiple_optimal_strategies_matrix", [1,2], does_not_raise()),
            ("equal_rows_and_solutions_matrix", [1,3], does_not_raise()),
            ("empty_matrix", None, pytest.raises(ValueError))   
        ]
    )
    def test_laplace_criterion(self, matrix, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderUncertainty.laplace_criterion(matrix)  == res

    @pytest.mark.parametrize(
        "matrix, res, expectation",
        [
            ("default_matrix", 3, does_not_raise()),
            ("big_matrix", 2, does_not_raise()),
            ("single_element_matrix", 1, does_not_raise()),
            ("multiple_optimal_strategies_matrix", 2, does_not_raise()),
            ("equal_rows_and_solutions_matrix", [1,3], does_not_raise()),
            ("empty_matrix", None, pytest.raises(ValueError))   
        ]
    )
    def test_maximax_criterion(self, matrix, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderUncertainty.maximax_criterion(matrix) == res

    @pytest.mark.parametrize(
        "matrix, alpha, res, expectation",
        [
            ("default_matrix", 0.5, 4, does_not_raise()),
            ("big_matrix", 0.5, 2, does_not_raise()),
            ("single_element_matrix", 0.5, 1, does_not_raise()),
            ("multiple_optimal_strategies_matrix", 0.5, 1, does_not_raise()),
            ("equal_rows_and_solutions_matrix", 0.5, [1,3], does_not_raise()),
            ("empty_matrix", 0.5, None, pytest.raises(ValueError))   
        ]
    )
    def test_hurwitz_criterion(self, matrix, alpha, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderUncertainty.hurwitz_criterion(matrix, alpha) == res