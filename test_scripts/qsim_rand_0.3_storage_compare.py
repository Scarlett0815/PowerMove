from Construct_Circuit import *
from mvqc import *
from enola import *
import random
import math

N_Qubit_List = [10, 20, 40, 60, 80]
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

no_storage_transfer_duration_list = []
no_storage_move_duration_list = [] 
no_storage_cir_fidelity_list = [] 
no_storage_cir_fidelity_1q_gate_list = [] 
no_storage_cir_fidelity_2q_gate_list = [] 
no_storage_cir_fidelity_2q_gate_for_idle_list = [] 
no_storage_cir_fidelity_atom_transfer_list = [] 
no_storage_cir_fidelity_coherence_list = []
no_storage_nstage_list = []

for n in N_Qubit_List:
    index = random.choice(I_List)
    Row = math.ceil(math.sqrt(n))

    test_circuit = QsimRandBenchmark(n, 10, 0.3, index).circ

    cz_blocks = get_cz_blocks(test_circuit)

    mvqc_transfer_duration, mvqc_move_duration, mvqc_cir_fidelity, mvqc_cir_fidelity_1q_gate, mvqc_cir_fidelity_2q_gate, mvqc_cir_fidelity_2q_gate_for_idle, mvqc_cir_fidelity_atom_transfer, mvqc_cir_fidelity_coherence, mvqc_nstage = mvqc(cz_blocks, Row, n, True)
    mvqc_transfer_duration_list.append(mvqc_transfer_duration)
    mvqc_move_duration_list.append(mvqc_move_duration)
    mvqc_cir_fidelity_list.append(mvqc_cir_fidelity)
    mvqc_cir_fidelity_1q_gate_list.append(mvqc_cir_fidelity_1q_gate)
    mvqc_cir_fidelity_2q_gate_list.append(mvqc_cir_fidelity_2q_gate)
    mvqc_cir_fidelity_2q_gate_for_idle_list.append(mvqc_cir_fidelity_2q_gate_for_idle)
    mvqc_cir_fidelity_atom_transfer_list.append(mvqc_cir_fidelity_atom_transfer)
    mvqc_cir_fidelity_coherence_list.append(mvqc_cir_fidelity_coherence)   
    mvqc_nstage_list.append(mvqc_nstage)

    no_storage_transfer_duration, no_storage_move_duration, no_storage_cir_fidelity, no_storage_cir_fidelity_1q_gate, no_storage_cir_fidelity_2q_gate, no_storage_cir_fidelity_2q_gate_for_idle, no_storage_cir_fidelity_atom_transfer, no_storage_cir_fidelity_coherence, no_storage_nstage = mvqc(cz_blocks, Row, n, False)
    no_storage_transfer_duration_list.append(no_storage_transfer_duration)
    no_storage_move_duration_list.append(no_storage_move_duration)
    no_storage_cir_fidelity_list.append(no_storage_cir_fidelity)
    no_storage_cir_fidelity_1q_gate_list.append(no_storage_cir_fidelity_1q_gate)
    no_storage_cir_fidelity_2q_gate_list.append(no_storage_cir_fidelity_2q_gate)
    no_storage_cir_fidelity_2q_gate_for_idle_list.append(no_storage_cir_fidelity_2q_gate_for_idle)
    no_storage_cir_fidelity_atom_transfer_list.append(no_storage_cir_fidelity_atom_transfer)
    no_storage_cir_fidelity_coherence_list.append(no_storage_cir_fidelity_coherence)  
    no_storage_nstage_list.append(no_storage_nstage)

with open("data/qsim_rand_0.3_storage_compare.txt", 'w') as file:
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

    file.write(str(no_storage_transfer_duration_list) + '\n') 
    file.write(str(no_storage_move_duration_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_1q_gate_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_2q_gate_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_2q_gate_for_idle_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_atom_transfer_list) + '\n') 
    file.write(str(no_storage_cir_fidelity_coherence_list) + '\n')
    file.write(str(no_storage_nstage_list) + '\n')

