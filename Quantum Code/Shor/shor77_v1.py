import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.circuit.library import QFT
#from qiskit.aqua.algorithms import Shor
from qiskit_aer import Aer
from math import gcd
import matplotlib.pyplot as plt
from fractions import Fraction

from qiskit.visualization import plot_histogram

# Function to create a controlled unitary corresponding to a^power % 77
def qpe_amod77(a, power):
    n = 7
    qc = QuantumCircuit(n)

    for _ in range(power):
        if a == 2:
            qc.swap(0, 1)
            qc.swap(1, 2)
            qc.swap(2, 3)
            qc.swap(3, 4)
            qc.swap(4, 5)
            qc.swap(5, 6)
        elif a == 3:
            qc.cswap(6, 0, 1)
            qc.cswap(6, 1, 2)
            qc.cswap(6, 2, 3)
            qc.cswap(6, 3, 4)
            qc.cswap(6, 4, 5)
            qc.cx(6, 6)
        elif a == 5 or a == 8:
            qc.swap(0, 1)
            qc.swap(1, 2)
            qc.swap(2, 3)
            qc.swap(3, 4)
            qc.swap(4, 5)
            qc.swap(5, 6)
        elif a == 7 or a == 13:
            qc.swap(0, 1)
            qc.swap(1, 2)
            qc.swap(2, 3)
            qc.swap(3, 4)
            qc.swap(4, 5)
            qc.swap(5, 6)
        elif a == 10:
            qc.swap(6, 0)
            qc.swap(5, 0)
            qc.swap(4, 0)
            qc.swap(3, 0)
            qc.swap(2, 0)
            qc.swap(1, 0)
        elif a == 11:
            qc.cswap(6, 0, 1)
            qc.cswap(6, 1, 2)
            qc.cswap(6, 2, 3)
            qc.cswap(6, 3, 4)
            qc.cswap(6, 4, 5)
            qc.cx(6, 6)
        elif a == 13:
            qc.swap(6, 0)
            qc.swap(5, 0)
            qc.swap(4, 0)
            qc.swap(3, 0)
            qc.swap(2, 0)
            qc.swap(1, 0)
        # Add gates for other values of 'a' as per required
        else:
            return None
    qc.name = "%i^%i mod 15" % (a, power)
    return qc.to_gate()

# Quantum Phase Estimation for Shor's Algorithm
def qpe(a):
    n = 7 + 7  # 7 qubits for the exponent and 7 for the result
    qc = QuantumCircuit(n, 7)

    # Initialize the result qubit to |1>
    qc.x(n-1)

    # Apply Hadamard gates to the counting qubits
    for qubit in range(7):
        qc.h(qubit)

    # Controlled-U gates
    for qubit in range(7):
        qc.append(qpe_amod77(a, 2**qubit).control(), [qubit] + list(range(7)))

    # Apply inverse QFT
    qc.append(QFT(7, do_swaps=False).inverse(), range(7, 14))

    # Measure the result
    qc.measure(range(7), range(7))

    return qc

# Function to execute Shor's algorithm for factoring 77
def shor_77():
    # Select random 'a' coprime with 77
    #coprimes = [a for a in range(2, 77) if gcd(a, 77) == 1]
    a = 13 #np.random.choice(coprimes)

    # Execute the Quantum Phase Estimation algorithm
    qc = qpe(a)
    backend = Aer.get_backend('qasm_simulator')
    qc.draw()
    qc_compiled = transpile(qc, backend)
    qobj = assemble(qc_compiled)
    result = backend.run(qobj).result()
    counts = result.get_counts()

    # Display the results
    plot_histogram(counts)
    plt.show()

    # Post-processing to find period "r" and factors of 77
    phases = [int(key, 2)/2**7 for key in counts.keys()]
    guesses = [round(1/phase) for phase in phases]

    for r in guesses:
        if r % 2 == 0:
            factor1 = gcd(a**(r//2) - 1, 77)
            factor2 = gcd(a**(r//2) + 1, 77)
            if factor1 != 1 and factor2 != 1:
                return factor1, factor2

    return None, None

# Run Shor's algorithm
factor1, factor2 = shor_77()
print(f"The factors of 77 are: {factor1} and {factor2}")