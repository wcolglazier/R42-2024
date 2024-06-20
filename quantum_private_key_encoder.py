from qiskit import QuantumCircuit
from qiskit_aer import Aer

def input_private_key():
    key = input("Enter a binary private key: ")
    if not set(key).issubset({'0', '1'}):
        raise ValueError("The key must be a binary string.")
    return key

def encode_key_in_circuit(key):
    key_length = len(key)
    qc = QuantumCircuit(key_length, key_length)
    for i, bit in enumerate(key):
        if bit == '1':
            qc.x(i)
    qc.measure(range(key_length), range(key_length))
    return qc

private_key = input_private_key()
print(f"Private Key: {private_key}")

circuit = encode_key_in_circuit(private_key)

print(circuit)
