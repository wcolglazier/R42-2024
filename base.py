import numpy as np
import pandas as pd
from cvxopt import matrix, solvers

# Expected returns for the two stocks (in decimals)
expected_returns = np.array([0.159, 0.012])

# Covariance matrix of the two stocks
cov_matrix = np.array([[0.046656, 0.0024],
                       [0.0024, 0.028561]])

# Number of assets
n = len(expected_returns)

# Convert numpy arrays to cvxopt matrices
P = matrix(cov_matrix)
q = matrix(np.zeros(n))

# Constraints Gx <= h
G = matrix(np.vstack((-expected_returns, -np.eye(n))))
h = matrix(np.hstack((-np.mean(expected_returns), np.zeros(n))))

# Constraints Ax = b
A = matrix(1.0, (1, n))
b = matrix(1.0)

# Solve the quadratic programming problem for minimum volatility
sol = solvers.qp(P, q, G, h, A, b)
min_vol_weights = np.array(sol['x'])

# Calculate the minimum volatility portfolio return and volatility
min_vol_return = np.dot(min_vol_weights.T, expected_returns)
min_vol_volatility = np.sqrt(np.dot(min_vol_weights.T, np.dot(cov_matrix, min_vol_weights)))

# Constraints for maximum Sharpe ratio (assuming risk-free rate is 0 for simplicity)
G_sharpe = matrix(-np.eye(n))
h_sharpe = matrix(np.zeros(n))

sol_sharpe = solvers.qp(P, -matrix(expected_returns), G_sharpe, h_sharpe, A, b)
max_sharpe_weights = np.array(sol_sharpe['x'])

# Calculate the maximum Sharpe ratio portfolio return and volatility
max_sharpe_return = np.dot(max_sharpe_weights.T, expected_returns)
max_sharpe_volatility = np.sqrt(np.dot(max_sharpe_weights.T, np.dot(cov_matrix, max_sharpe_weights)))

# Creating the output table
data = {
    'Annualised Return (%)': [expected_returns[0] * 100, expected_returns[1] * 100],
    'Annualised Volatility (%)': [np.sqrt(cov_matrix[0, 0]) * 100, np.sqrt(cov_matrix[1, 1]) * 100],
    'Max Sharpe Ratio (% weights)': [max_sharpe_weights[0] * 100, max_sharpe_weights[1] * 100],
    'Min Volatility (% weights)': [min_vol_weights[0] * 100, min_vol_weights[1] * 100]
}

df = pd.DataFrame(data, index=['Stock 1', 'Stock 2'])

# Print the DataFrame
print(df)

# Print overall portfolio metrics
print("\nMinimum Volatility Portfolio:")
print(f"Return: {min_vol_return[0] * 100:.2f}%")
print(f"Volatility: {min_vol_volatility[0, 0] * 100:.2f}%")  # Access the scalar value correctly

print("\nMaximum Sharpe Ratio Portfolio:")
print(f"Return: {max_sharpe_return[0] * 100:.2f}%")
print(f"Volatility: {max_sharpe_volatility[0, 0] * 100:.2f}%")  # Access the scalar value correctly
