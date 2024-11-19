from Construct_Circuit import *
from mvqc import *
from enola import *
import qiskit.qasm2
import random
import math
import time

N_Qubit_List = [30, 40, 50, 60, 80]
I_List = range(10)

mvqc_runtime = []

enola_runtime = []
p = 0.5
index = random.choice(I_List)
type = 'regular'
for n in N_Qubit_List:
    Row = math.ceil(math.sqrt(n))

    path = f"qaoa/{type}/q{n}_regular4/i{index}.txt"


    with open(path, "r") as fid:
        gates = eval(fid.read())
    
    mvqc_start_time = time.time()
    mvqc_transfer_duration, mvqc_move_duration, mvqc_cir_fidelity, mvqc_cir_fidelity_1q_gate, mvqc_cir_fidelity_2q_gate, mvqc_cir_fidelity_2q_gate_for_idle, mvqc_cir_fidelity_atom_transfer, mvqc_cir_fidelity_coherence, mvqc_nstage = mvqc([gates], Row, n, False)
    mvqc_runtime.append(time.time() - mvqc_start_time)

    enola_start_time = time.time()
    enola_transfer_duration, enola_move_duration, enola_cir_fidelity, enola_cir_fidelity_1q_gate, enola_cir_fidelity_2q_gate, enola_cir_fidelity_2q_gate_for_idle, enola_cir_fidelity_atom_transfer, enola_cir_fidelity_coherence, enola_nstage = enola([gates], Row, n)
    enola_runtime.append(time.time() - enola_start_time)
print(mvqc_runtime)
print(enola_runtime)