from Construct_Circuit import *
from mvqc import *
from enola import *
import qiskit.qasm2
import random
import math
import time

N_Qubit_List = [10, 20, 40]
I_List = range(10)

mvqc_runtime = []

enola_runtime = []
p = 0.5
index = random.choice(I_List)
type = 'rand'
for n in N_Qubit_List:
    Row = math.ceil(math.sqrt(n))

    test_circuit = QsimRandBenchmark(n, 10, 0.3, index).circ

    cz_blocks = get_cz_blocks(test_circuit)

    mvqc_start_time = time.time()
    mvqc_transfer_duration, mvqc_move_duration, mvqc_cir_fidelity, mvqc_cir_fidelity_1q_gate, mvqc_cir_fidelity_2q_gate, mvqc_cir_fidelity_2q_gate_for_idle, mvqc_cir_fidelity_atom_transfer, mvqc_cir_fidelity_coherence, mvqc_nstage = mvqc(cz_blocks, Row, n, False)
    mvqc_runtime.append(time.time() - mvqc_start_time)

    enola_start_time = time.time()
    enola_transfer_duration, enola_move_duration, enola_cir_fidelity, enola_cir_fidelity_1q_gate, enola_cir_fidelity_2q_gate, enola_cir_fidelity_2q_gate_for_idle, enola_cir_fidelity_atom_transfer, enola_cir_fidelity_coherence, enola_nstage = enola(cz_blocks, Row, n)
    enola_runtime.append(time.time() - enola_start_time)
print(mvqc_runtime)
print(enola_runtime)