import numpy as np

class DecisionMakingUnderUncertainty:
    
    @staticmethod
    def wald_criterion(payoff_matrix):
        min_row = np.min(payoff_matrix, axis=1)
        solution = np.argmax(min_row) + 1
        return solution

    @staticmethod
    def laplace_criterion(payoff_matrix):
        mean_row = np.mean(payoff_matrix, axis=1)
        solution = np.argmax(mean_row) + 1
        return solution

    @staticmethod
    def maximax_criterion(payoff_matrix):
        max_row = np.max(payoff_matrix, axis=1)
        solution = np.argmax(max_row) + 1
        return solution

    @staticmethod
    def hurwitz_criterion(payoff_matrix, alpha):
        min_row = alpha * np.min(payoff_matrix, axis=1)
        max_row = (1 - alpha) * np.max(payoff_matrix, axis=1)
        solution = np.argmax(min_row + max_row) + 1
        return solution