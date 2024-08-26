import numpy as np

class DecisionMakingUnderRisk:

    @staticmethod
    def bayes_laplace_criterio(payoff_matrix):
        if payoff_matrix.size == 0:
            raise ValueError("The matrix is empty")
        if np.sum(payoff_matrix[0]) != 1:
            raise ValueError("The sum of the probabilities must be 1")
        expected_value_row = np.sum(payoff_matrix[1:]*payoff_matrix[0],axis=1)
        solution = np.flatnonzero(expected_value_row == np.max(expected_value_row)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)
    
    @staticmethod
    def germeyer_criterio(payoff_matrix, c_value):
        if payoff_matrix.size == 0:
            raise ValueError("The matrix is empty")
        if np.sum(payoff_matrix[0]) != 1:
            raise ValueError("The sum of the probabilities must be 1")
        max_element = np.max(payoff_matrix[1:])
        weights = payoff_matrix[0]
        new_matrix = payoff_matrix[1:] - max_element*c_value
        min_expected_value_rows = np.min(new_matrix*weights,axis=1)
        solution = np.flatnonzero(min_expected_value_rows == np.max(min_expected_value_rows)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)   
    
    @staticmethod
    def hodge_lehmann_criterio(payoff_matrix, alpha):
        if payoff_matrix.size == 0:
            raise ValueError("The matrix is empty")
        if np.sum(payoff_matrix[0]) != 1:
            raise ValueError("The sum of the probabilities must be 1")
        expected_value_row = alpha*np.sum(payoff_matrix[1:]*payoff_matrix[0],axis=1)
        min_row = (1-alpha)*np.min(payoff_matrix[1:], axis=1)
        combined = expected_value_row + min_row
        solution = np.flatnonzero(combined == np.max(combined)) + 1
        if solution.size == 1:
            return solution[0]
        else:
            return list(solution)