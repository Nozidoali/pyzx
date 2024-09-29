from qiskit.quantum_info import Statevector
from qiskit import qasm2

# load from adder.qasm

import numpy as np

def get(s):
    for i, v in enumerate(s):
        if np.isclose(v, 1):
            # return binary representation of i
            return bin(i)[2:].zfill(10)
        
if __name__ == "__main__":
    qc = qasm2.load("./adder.qasm")
    # Set the initial state to 100,000,000 for 9 qubits before running qc
    for a in range(1, 2**3):
        for b in range(1, 2**3):
            # the ten bits are: 
            # 0, a[0], b[0], c[0], a[1], b[1], c[1], a[2], b[2], c[2]
            in_patterns = [0] + [bit for i in range(3) for bit in [(a>>i)&1, (b>>i)&1, 0]]
            in_str = "".join([str(bit) for bit in in_patterns])[::-1]
            print(in_str)
            
            initial_state_vector = Statevector.from_label(in_str)
            final_state = initial_state_vector.evolve(qc)
            s = get(final_state.data)
            print(s)
            
            c = int(s[9]) * 4 + int(s[6]) * 2 + int(s[3])

            print(f"{a} + {b} = {c}")