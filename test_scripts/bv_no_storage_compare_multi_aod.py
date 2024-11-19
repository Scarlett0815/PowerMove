from Construct_Circuit import *
from mvqc_multi_aod import *
from enola import *
import qiskit.qasm2
import random
import math

NAOD_list = [1, 2, 3, 4]
N_Qubit_List = [14, 50, 70]
I_List = range(10)


# p = random.choice(P_List)
index = random.choice(I_List)

with open("data/bv_no_storage_compare_multi_aod.txt", 'w') as file:
    file.write(str(NAOD_list) + '\n')
    for NAOD in NAOD_list:
        mvqc_transfer_duration_list = []
        mvqc_move_duration_list = [] 
        mvqc_cir_fidelity_list = [] 
        mvqc_cir_fidelity_1q_gate_list = [] 
        mvqc_cir_fidelity_2q_gate_list = [] 
        mvqc_cir_fidelity_2q_gate_for_idle_list = [] 
        mvqc_cir_fidelity_atom_transfer_list = [] 
        mvqc_cir_fidelity_coherence_list = []
        mvqc_nstage_list = []
        for n in N_Qubit_List:
            index = random.choice(I_List)
            Row = math.ceil(math.sqrt(n))

            circ = QuantumCircuit.from_qasm_file(f"bv/bv_n{n}.qasm")
            test_circuit = transpile(circ, basis_gates=["u1", "u2", "u3", "cz", "id"])

            cz_blocks = get_cz_blocks(test_circuit)

            mvqc_transfer_duration, mvqc_move_duration, mvqc_cir_fidelity, mvqc_cir_fidelity_1q_gate, mvqc_cir_fidelity_2q_gate, mvqc_cir_fidelity_2q_gate_for_idle, mvqc_cir_fidelity_atom_transfer, mvqc_cir_fidelity_coherence, mvqc_nstage = mvqc(cz_blocks, Row, n, False, NAOD)
            mvqc_transfer_duration_list.append(mvqc_transfer_duration)
            mvqc_move_duration_list.append(mvqc_move_duration)
            mvqc_cir_fidelity_list.append(mvqc_cir_fidelity)
            mvqc_cir_fidelity_1q_gate_list.append(mvqc_cir_fidelity_1q_gate)
            mvqc_cir_fidelity_2q_gate_list.append(mvqc_cir_fidelity_2q_gate)
            mvqc_cir_fidelity_2q_gate_for_idle_list.append(mvqc_cir_fidelity_2q_gate_for_idle)
            mvqc_cir_fidelity_atom_transfer_list.append(mvqc_cir_fidelity_atom_transfer)
            mvqc_cir_fidelity_coherence_list.append(mvqc_cir_fidelity_coherence)   
            mvqc_nstage_list.append(mvqc_nstage)

        file.write(str(N_Qubit_List) + '\n')
        file.write(str(mvqc_transfer_duration_list) + '\n') 
        file.write(str(mvqc_move_duration_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_1q_gate_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_2q_gate_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_2q_gate_for_idle_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_atom_transfer_list) + '\n') 
        file.write(str(mvqc_cir_fidelity_coherence_list) + '\n')
        file.write(str(mvqc_nstage_list) + '\n')
