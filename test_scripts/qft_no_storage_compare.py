from Construct_Circuit import *
from mvqc import *
from enola import *
import qiskit.qasm2
import random
import math

N_Qubit_List = [18, 29, 63]
I_List = range(10)

mvqc_transfer_duration_list = []
mvqc_move_duration_list = [] 
mvqc_cir_fidelity_list = [] 
mvqc_cir_fidelity_1q_gate_list = [] 
mvqc_cir_fidelity_2q_gate_list = [] 
mvqc_cir_fidelity_2q_gate_for_idle_list = [] 
mvqc_cir_fidelity_atom_transfer_list = [] 
mvqc_cir_fidelity_coherence_list = []
mvqc_nstage_list = []

enola_transfer_duration_list = []
enola_move_duration_list = [] 
enola_cir_fidelity_list = [] 
enola_cir_fidelity_1q_gate_list = [] 
enola_cir_fidelity_2q_gate_list = [] 
enola_cir_fidelity_2q_gate_for_idle_list = [] 
enola_cir_fidelity_atom_transfer_list = [] 
enola_cir_fidelity_coherence_list = []
enola_nstage_list = []

for n in N_Qubit_List:
    index = random.choice(I_List)
    Row = math.ceil(math.sqrt(n))

    circ = QuantumCircuit.from_qasm_file(f"qft/qft_n{n}.qasm")
    test_circuit = transpile(circ, basis_gates=["u1", "u2", "u3", "cz", "id"],  optimization_level=2)

    cz_blocks = get_cz_blocks(test_circuit)

    mvqc_transfer_duration, mvqc_move_duration, mvqc_cir_fidelity, mvqc_cir_fidelity_1q_gate, mvqc_cir_fidelity_2q_gate, mvqc_cir_fidelity_2q_gate_for_idle, mvqc_cir_fidelity_atom_transfer, mvqc_cir_fidelity_coherence, mvqc_nstage = mvqc(cz_blocks, Row, n, False)
    mvqc_transfer_duration_list.append(mvqc_transfer_duration)
    mvqc_move_duration_list.append(mvqc_move_duration)
    mvqc_cir_fidelity_list.append(mvqc_cir_fidelity)
    mvqc_cir_fidelity_1q_gate_list.append(mvqc_cir_fidelity_1q_gate)
    mvqc_cir_fidelity_2q_gate_list.append(mvqc_cir_fidelity_2q_gate)
    mvqc_cir_fidelity_2q_gate_for_idle_list.append(mvqc_cir_fidelity_2q_gate_for_idle)
    mvqc_cir_fidelity_atom_transfer_list.append(mvqc_cir_fidelity_atom_transfer)
    mvqc_cir_fidelity_coherence_list.append(mvqc_cir_fidelity_coherence)   
    mvqc_nstage_list.append(mvqc_nstage)

    enola_transfer_duration, enola_move_duration, enola_cir_fidelity, enola_cir_fidelity_1q_gate, enola_cir_fidelity_2q_gate, enola_cir_fidelity_2q_gate_for_idle, enola_cir_fidelity_atom_transfer, enola_cir_fidelity_coherence, enola_nstage = enola(cz_blocks, Row, n)
    enola_transfer_duration_list.append(enola_transfer_duration)
    enola_move_duration_list.append(enola_move_duration)
    enola_cir_fidelity_list.append(enola_cir_fidelity)
    enola_cir_fidelity_1q_gate_list.append(enola_cir_fidelity_1q_gate)
    enola_cir_fidelity_2q_gate_list.append(enola_cir_fidelity_2q_gate)
    enola_cir_fidelity_2q_gate_for_idle_list.append(enola_cir_fidelity_2q_gate_for_idle)
    enola_cir_fidelity_atom_transfer_list.append(enola_cir_fidelity_atom_transfer)
    enola_cir_fidelity_coherence_list.append(enola_cir_fidelity_coherence)  
    enola_nstage_list.append(enola_nstage)
with open("data/qft_no_storage_compare.txt", 'w') as file:
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

    file.write(str(enola_transfer_duration_list) + '\n') 
    file.write(str(enola_move_duration_list) + '\n') 
    file.write(str(enola_cir_fidelity_list) + '\n') 
    file.write(str(enola_cir_fidelity_1q_gate_list) + '\n') 
    file.write(str(enola_cir_fidelity_2q_gate_list) + '\n') 
    file.write(str(enola_cir_fidelity_2q_gate_for_idle_list) + '\n') 
    file.write(str(enola_cir_fidelity_atom_transfer_list) + '\n') 
    file.write(str(enola_cir_fidelity_coherence_list) + '\n')
    file.write(str(enola_nstage_list) + '\n')
