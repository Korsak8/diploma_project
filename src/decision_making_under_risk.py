import numpy as np

class DecisionMakingUnderRisk:

    @staticmethod
    def bayes_laplace_criterio(payoff_matrix):
        expeced_value_row = np.sum(payoff_matrix[1:]*payoff_matrix[0],axis=1)
        solution = np.argmax(expeced_value_row) + 1
        return solution
    
    @staticmethod
    def germeyer_criterio(payoff_matrix):
        max_element = np.max(payoff_matrix[1:])
        new_matrix = payoff_matrix[1:] - max_element*2
        weights = payoff_matrix[0]
        expeced_value_row = np.sum(new_matrix*weights,axis=1)
        solution = np.argmax(expeced_value_row) + 1
        return solution
    
    @staticmethod
    def hodge_lehmann_criterio(payoff_matrix, alpha):
        expeced_value_row = alpha*np.sum(payoff_matrix[1:]*payoff_matrix[0],axis=1)
        min_row = (1-alpha)*np.min(payoff_matrix, axis=1)
        solution = np.argmax(expeced_value_row+min_row) + 1
        return solution