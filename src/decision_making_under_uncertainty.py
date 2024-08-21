import numpy as np

class DecisionMakingUnderUncertainty:
    
    @staticmethod
    def wald_criterion(payoff_matrix):
        if payoff_matrix.ndim == 1 and payoff_matrix.shape[0] != 0:
            return 1
        min_row = np.min(payoff_matrix, axis=1)
        solution = np.flatnonzero(min_row == np.max(min_row)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)

    @staticmethod
    def laplace_criterion(payoff_matrix):
        if payoff_matrix.ndim == 1 and payoff_matrix.shape[0] != 0:
            return 1
        mean_row = np.mean(payoff_matrix, axis=1)
        solution = np.flatnonzero(mean_row == np.max(mean_row)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)

    @staticmethod
    def maximax_criterion(payoff_matrix):
        if payoff_matrix.ndim == 1 and payoff_matrix.shape[0] != 0:
            return 1
        max_row = np.max(payoff_matrix, axis=1)
        solution = np.flatnonzero(max_row == np.max(max_row)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)

    @staticmethod
    def hurwitz_criterion(payoff_matrix, alpha):
        if payoff_matrix.ndim == 1 and payoff_matrix.shape[0] != 0:
            return 1
        min_row = alpha * np.min(payoff_matrix, axis=1)
        max_row = (1 - alpha) * np.max(payoff_matrix, axis=1)
        combined = min_row + max_row
        solution = np.flatnonzero(combined == np.max(combined)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)