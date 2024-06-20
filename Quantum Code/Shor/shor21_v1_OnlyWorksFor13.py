import numpy as np
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.circuit.library import QFT
#from qiskit.aqua.algorithms import Shor
from qiskit_aer import Aer
from math import gcd
import matplotlib.pyplot as plt
from fractions import Fraction

from qiskit.visualization import plot_histogram

# Function to implement the controlled modular exponentiation for specific 'a'
def qpe_amod21(a, power):
    qc = QuantumCircuit(5)
    if a == 2:
        qc = apply_controlled_unitary_mod_21(qc, [2] * power)
    elif a == 4:
        qc = apply_controlled_unitary_mod_21(qc, [4] * power)
    elif a == 5:
        qc = apply_controlled_unitary_mod_21(qc, [5] * power)
    elif a == 8:
        qc = apply_controlled_unitary_mod_21(qc, [8] * power)
    elif a == 10:
        qc = apply_controlled_unitary_mod_21(qc, [10] * power)
    elif a == 11:
        qc = apply_controlled_unitary_mod_21(qc, [11] * power)
    elif a == 13:
        qc = apply_controlled_unitary_mod_21(qc, [13] * power)
    elif a == 16:
        qc = apply_controlled_unitary_mod_21(qc, [16] * power)
    elif a == 17:
        qc = apply_controlled_unitary_mod_21(qc, [17] * power)
    elif a == 19:
        qc = apply_controlled_unitary_mod_21(qc, [19] * power)
    elif a == 20:
        qc = apply_controlled_unitary_mod_21(qc, [20] * power)
    return qc

def apply_controlled_unitary_mod_21(qc, a_list):
    # This function repeatedly multiplies by 'a' modulo 21.
    for a in a_list:
        if a == 2:
            qc.swap(2, 3)
            qc.swap(1, 2)
            qc.swap(0, 1)
        elif a == 4:
            qc.swap(1, 3)
            qc.swap(0, 2)
        elif a == 5:
            qc.cx(4, 3)
            qc.cx(4, 2)
        elif a == 8:
            qc.swap(0, 1)
            qc.swap(1, 2)
            qc.swap(2, 3)
        elif a == 10:
            qc.cx(4, 3)
            qc.cx(4, 1)
        elif a == 11:
            qc.swap(1, 3)
            qc.cx(4, 2)
        elif a == 13:
            qc.cx(4, 3)
            qc.cx(4, 1)
        elif a == 16:
            qc.swap(0, 1)
            qc.swap(1, 2)
            qc.swap(2, 3)
        elif a == 17:
            qc.cx(4, 3)
            qc.cx(4, 2)
        elif a == 19:
            qc.cx(4, 2)
            qc.cx(4, 1)
        elif a == 20:
            qc.cx(4, 3)
            qc.cx(4, 0)
    return qc

def qft_dagger(qc, n):
    for qubit in range(n//2):
        qc.swap(qubit, n-qubit-1)
    for qubit in range(n):
        for k in range(qubit):
            qc.cp(-np.pi/float(2**(qubit-k)), k, qubit)
        qc.h(qubit)

# Function to compute the modular inverse
def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Main function to run Shor's algorithm
def shors_algorithm(N):
    np.random.seed(1)

    # Choose a random 'a' such that gcd(a, N) == 1
    for _ in range(10):
        a = np.random.randint(2, N)
        while np.gcd(a, N) != 1:
            a = np.random.randint(2, N)
        a = 17
        print(f"Chosen a = {a}")

        # Quantum Phase Estimation
        qpe_circ = QuantumCircuit(10, 5)
        qpe_circ.h(range(5))
        qpe_circ.x(10-1)

        for qubit in range(5):
            unitary = qpe_amod21(a, 2**qubit).to_gate()
            controlled_unitary = unitary.control()
            qpe_circ.append(controlled_unitary, [qubit] + [i + 5 for i in range(5)])

        qft_dagger(qpe_circ, 5)
        qpe_circ.measure(range(5), range(5))

        aer_sim = Aer.get_backend('aer_simulator')
        qobj = assemble(transpile(qpe_circ, aer_sim))
        result = aer_sim.run(qobj).result()
        counts = result.get_counts()
        print("Counts:", counts)
        measured_phases = [int(state, 2) / 2**5 for state in counts]

        period_candidates = []
        for phase in measured_phases:
            if np.isclose(phase, 0):
                continue
            frac = Fraction(phase).limit_denominator(N)
            r = frac.denominator
            if pow(a, r, N) == 1:
                period_candidates.append(r)

        if period_candidates:
            r = min(period_candidates)
            print(f"Period r = {r}")
            if r % 2 != 0:
                continue
            possible_factor_1 = np.gcd(pow(a, r//2) - 1, N)
            possible_factor_2 = np.gcd(pow(a, r//2) + 1, N)
            if possible_factor_1 == 1 or possible_factor_1 == N:
                possible_factor_1 = None
            if possible_factor_2 == 1 or possible_factor_2 == N:
                possible_factor_2 = None
            if possible_factor_1 or possible_factor_2:
                return possible_factor_1, possible_factor_2
    return None, None

# Running Shor's algorithm for N = 21
f1, f2 = shors_algorithm(21)
if f1 and f2:
    print(f"Factors of 21: {f1} and {f2}")
else:
    print("Failed to factorize 21")