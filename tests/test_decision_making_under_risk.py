import pytest
import numpy as np
from src.decision_making_under_risk import DecisionMakingUnderRisk
from contextlib import nullcontext as does_not_raise

@pytest.fixture
def default_matrix():
    return np.array([
    [0.15, 0.3, 0.35, 0.2],
    [3200, 4500, 5100, 3300],
    [4900, 3100, 5300, 4700],
    [3400, 5200, 3600, 5400],
    [4000, 3500, 5350, 3700],
    [3000, 4600, 5000, 3800]
    ])

@pytest.fixture
def big_matrix():
    return np.array([
    [0.4, 0.15, 0.1, 0.1, 0.05, 0.15, 0.05],
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
    return np.array([
    [1],
    [1]
    ])

@pytest.fixture
def equal_rows_multiple_solutions_matrix():
    return np.array([
        [0.2, 0.35, 0.25, 0.2],
        [4100, 4500, 3900, 4800],
        [3700, 4100, 4300, 3600],
        [4100, 4500, 3900, 4800],
        [3850, 4200, 4100, 4500],
        [3600, 3900, 3700, 4600]
    ])

@pytest.fixture
def empty_matrix():
    return np.array([])

@pytest.fixture
def probability_sum_not_one_matrix():
    return np.array([
        [0.4, 0.2, 0.7],
        [3400, 2700, 3200],
        [3100,2900,3000],
        [2700,3000,3300]
    ])

class TestDecisionMakingUnderRisk():
    @pytest.mark.parametrize(
        "matrix, res, expectation",
        [
            ("default_matrix", 2, does_not_raise()),
            ("big_matrix", 4, does_not_raise()),
            ("single_element_matrix", 1, does_not_raise()),
            ("equal_rows_multiple_solutions_matrix", [1,3], does_not_raise()),
            ("empty_matrix", None, pytest.raises(ValueError)),
            ("probability_sum_not_one_matrix", None, pytest.raises(ValueError))
        ]
    )
    def test_bayes_laplace_criterio(self, matrix, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderRisk.bayes_laplace_criterio(matrix) == res

    @pytest.mark.parametrize(
        "matrix, c_value, res, expectation",
        [
            ("default_matrix", 2, 1, does_not_raise()),
            ("big_matrix", 1.5, 4, does_not_raise()),
            ("single_element_matrix", 1.9, 1, does_not_raise()),
            ("equal_rows_multiple_solutions_matrix", 1.8, [1,3], does_not_raise()),
            ("empty_matrix", 1.2, None, pytest.raises(ValueError)),
            ("probability_sum_not_one_matrix", 2.3, None, pytest.raises(ValueError))
        ]
    )
    def test_germeyer_criterio(self, matrix, c_value, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderRisk.germeyer_criterio(matrix, c_value) == res

    @pytest.mark.parametrize(
        "matrix, alpha, res, expectation",
        [
            ("default_matrix", 0.5, 3,  does_not_raise()),
            ("big_matrix", 0.5, 4, does_not_raise()),
            ("single_element_matrix", 0.5, 1, does_not_raise()),
            ("equal_rows_multiple_solutions_matrix", 0.5, [1,3], does_not_raise()),
            ("empty_matrix", 0.5, None, pytest.raises(ValueError)),
            ("probability_sum_not_one_matrix", 0.5, None, pytest.raises(ValueError))
        ]
    )
    def test_hodge_lehmann_criterio(self, matrix, alpha, res, expectation, request):
        matrix = request.getfixturevalue(matrix)
        with expectation:
            assert DecisionMakingUnderRisk.hodge_lehmann_criterio(matrix, alpha) == res