import datetime
import numpy as np
import matplotlib.pyplot as plt
from qiskit_aer import Aer
from qiskit_algorithms import VQE, QAOA
from qiskit_algorithms.utils import algorithm_globals
from qiskit_algorithms.optimizers import COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit_finance.applications.optimization import PortfolioOptimization
from qiskit.primitives import Estimator
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.primitives import Sampler

# Set parameters
num_assets = 4  # number of assets, updated to match your data
q = 0.9  # risk factor from 1 to 0
budget = num_assets # budget to select exactly 1 out of 2 assets
seed = 321  # random seed

# Expected returns and covariance matrix for the two stocks
expected_returns = np.array([0.15, 0.08, 0.12, 0.10])

cov_matrix = np.array([[0.025, 0.006, 0.008, 0.005],
                       [0.006, 0.020, 0.007, 0.004],
                       [0.008, 0.007, 0.030, 0.009],
                       [0.005, 0.004, 0.009, 0.018]])

# Visualize the covariance matrix
plt.imshow(cov_matrix, interpolation='nearest')
plt.colorbar()
plt.title("Covariance Matrix")
plt.show()

# Define Portfolio Optimization Problem
portfolio = PortfolioOptimization(expected_returns=expected_returns, covariances=cov_matrix, risk_factor=q, budget=budget)
qp = portfolio.to_quadratic_program()
print(qp)

# Define the VQE Solver
algorithm_globals.random_seed = seed
cobyla = COBYLA(maxiter=100)
ry = TwoLocal(num_assets, "ry", "cz", reps=3, entanglement="full")
estimator = Estimator()
sampler = Sampler()

# Perform VQE
vqe = VQE(estimator=estimator, ansatz=ry, optimizer=cobyla)
qaoa = QAOA(sampler=sampler, optimizer=cobyla)
vqe_solver = MinimumEigenOptimizer(qaoa)

# Solve the problem
result = vqe_solver.solve(qp)
print(result)

# Print the optimized portfolio
selection = [f"STOCK{i}" for i in range(num_assets) if result.x[i] > 0.5]
print("Optimized Portfolio:", selection)

# Visualization of the optimized portfolio results
# Bar plot for expected returns
plt.figure(figsize=(10, 5))
plt.bar([f'STOCK{i}' for i in range(num_assets)], expected_returns)
plt.title('Expected Returns of Stocks')
plt.xlabel('Stocks')
plt.ylabel('Expected Return')
plt.show()

# Display the results
print("Results:")
print(f"Objective function value (fval): {result.fval}")
for i in range(num_assets):
    print(f"Stock {i} weight: {result.x[i]}")

# Visualize the optimized portfolio composition
labels = [f'STOCK{i}' for i in range(num_assets)]
sizes = result.x
explode = [0.1 if s > 0.5 else 0 for s in sizes]  # explode the selected stocks

plt.figure(figsize=(7, 7))
plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
plt.title('Optimized Portfolio Composition')
plt.axis('equal')
plt.show()
