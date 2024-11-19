import numpy as np
from qiskit import QuantumCircuit, transpile

def get_cz_blocks(circuit):
    qubit_cz_gate_map = {}
    qubit_depth_map = {}
    cz_gates = {}

    for i in range(circuit.num_qubits):
        qubit_depth_map[i] = 0

    cz_index = 0
    for instr, qargs, _ in circuit.data:
        if instr.name == 'cz':
            
            control, target = [qubit._index for qubit in qargs]
            # print("gate", control, target)
            qubit_cz_gate_map[(control, cz_index)] = qubit_depth_map[control]
            # print(control, cz_index, qubit_depth_map[control])
    
            qubit_cz_gate_map[(target, cz_index)] = qubit_depth_map[target]
            # print(target, cz_index, qubit_depth_map[target])

            cz_gates[cz_index] = (control, target)
            # print((control, target))
            cz_index += 1
        else:
            q = [qubit._index for qubit in qargs][0]
            qubit_depth_map[q] += 1

    # print(cz_index)
    # print(qubit_cz_gate_map)
    # print(cz_gates)
    cz_blocks = []
    for i in range(cz_index):
        gate = cz_gates[i]
        find_flag = False
        for cz_block_i in range(len(cz_blocks)):
            find_flag = True
            for cz_i in cz_blocks[cz_block_i]:
                cz_gate = cz_gates[cz_i]
                if cz_gate[0] == gate[0]:
                    if qubit_cz_gate_map[(cz_gate[0], i)] != qubit_cz_gate_map[(gate[0], cz_i)]:
                        find_flag = False
                        break
                if cz_gate[0] == gate[1]:
                    if qubit_cz_gate_map[(cz_gate[0], i)] != qubit_cz_gate_map[(gate[1], cz_i)]:
                        find_flag = False
                        break                    
                if cz_gate[1] == gate[0]:
                    if qubit_cz_gate_map[(cz_gate[1], i)] != qubit_cz_gate_map[(gate[0], cz_i)]:
                        find_flag = False
                        break
                if cz_gate[1] == gate[1]:
                    if qubit_cz_gate_map[(cz_gate[1], i)] != qubit_cz_gate_map[(gate[1], cz_i)]:
                        find_flag = False
                        break   
            if find_flag:
                # print(i)
                cz_blocks[cz_block_i].append(i)
                break

        if not find_flag:
            cz_blocks.append([i])
    blocks = []
    for cz_block in cz_blocks:
        blocks.append([])
        for i in cz_block:
            blocks[-1].append(cz_gates[i])      

    return blocks

def pauli_strings_to_qiskit_circuit(pauli_strings, keep_length=None):
    if keep_length is not None:
        pauli_strings = pauli_strings[:keep_length]
    circ = QuantumCircuit(len(pauli_strings[0]))
    for paulis in pauli_strings:
        plist = []
        for i in range(len(paulis)):
            if paulis[i] == "X":
                circ.h(i)
                plist.append(i)
            elif paulis[i] == "Y":
                circ.h(i)
                circ.sdg(i)
                plist.append(i)
            elif paulis[i] == "Z":
                plist.append(i)
        if len(plist) > 1:
            for i in plist[1:]:
                circ.cx(i, plist[0])
            circ.rz(np.pi / 8, plist[0])  # change to an rather arbitrary angle
            for i in plist[1:]:
                circ.cx(i, plist[0])
        elif len(plist) == 1:
            circ.rz(np.pi / 8, plist[0])
        for i in range(len(paulis)):
            if paulis[i] == "X":
                circ.h(i)
            elif paulis[i] == "Y":
                circ.s(i)
                circ.h(i)
            elif paulis[i] == "Z":
                pass
    circ = transpile(circ, basis_gates=["u3", "id", "cz"], optimization_level = 2)
    return circ

class QsimRandBenchmark():
    def __init__(self, n_qubits, keep_length, p, i):
        super().__init__()
        self.n_qubits = n_qubits
        self.keep_length = keep_length
        self.p = p
        self.i = i
        self.path = f"qsim/rand/q{n_qubits}_{keep_length}_p{p}/i{i}.txt"
        print(self.path)

        with open(self.path, "r") as fid:
            self.pauli_strings = eval(fid.read())[0:keep_length]

        self.circ = pauli_strings_to_qiskit_circuit(
            self.pauli_strings, keep_length=self.keep_length
        )

def QFT(n):
    circ = QuantumCircuit(n)
    
    # Apply the QFT algorithm using CZ and single-qubit gates
    for j in range(n):
        circ.h(j)
        for k in range(j + 1, n):
            angle = np.pi / (2 ** (k - j))
            circ.rz(angle, k)
            circ.cz(j, k)
        circ.rz(np.pi / 2, j)  # Extra phase for alignment

    # Decompose the SWAP gates using CZ and H
    for j in range(n // 2):
        circ.h(j)
        circ.cz(j, n - j - 1)
        circ.h(j)
        circ.h(n - j - 1)
        circ.cz(n - j - 1, j)
        circ.h(n - j - 1)
        circ.h(j)
        circ.cz(j, n - j - 1)
        circ.h(j)
    return circ