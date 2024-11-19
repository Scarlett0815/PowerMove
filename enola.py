from scheduler.gate_scheduler import gate_scheduling
from placer.placer import place_qubit
from router.router import route_qubit
import math

Infinity = math.inf
Fidelity_2Q_Gate = 0.995
Fidelity_1Q_Gate = 0.995
Fidelity_Atom_Transfer = 0.999
Coherence_Time = 1.5e6 # ms

def storage_gate_scheduling(gates, storage_flag):
    # print(gates)
    colored_gates = []
    for g in gates:
        new_color = True
        i = 0
        # colored_gates.sort(key = len)
        # print("color gates", colored_gates)
        for cgs in colored_gates:
            conflict_flag = False
            for cg in cgs:
                if g[0] == cg[0]:
                    conflict_flag = True
                    break
                elif g[0] == cg[1]:
                    conflict_flag = True
                    break
                elif g[1] == cg[0]:
                    conflict_flag = True
                    break
                elif g[1] == cg[1]:
                    conflict_flag = True
                    break
            if not conflict_flag:
                new_color = False
                colored_gates[i].append(g)
                break
            i += 1
        if new_color:
            colored_gates.append([g])
    if storage_flag:
        colored_gates.sort(key = len)
        lg = []
        color_num = len(colored_gates)
        for i in range(color_num):
            if i == 0:
                mg = colored_gates[0]
                lg.append(mg)
                colored_gates.remove(mg)
            else:
                min_diff = Infinity
                pre_mg = lg[-1]
                target_mg = []
                for mg in colored_gates:
                    pre_interaction_qubits = []
                    for m in pre_mg:
                        pre_interaction_qubits.append(m[0])
                        pre_interaction_qubits.append(m[1]) 
                    interaction_qubits = []
                    for m in mg:
                        interaction_qubits.append(m[0])
                        interaction_qubits.append(m[1])     
                    cur_diff = 0
                    for q in interaction_qubits:
                        if q not in pre_interaction_qubits:
                            cur_diff += 1

                    # for q in pre_interaction_qubits:
                    #     if q not in interaction_qubits:
                    #         cur_diff += 0.1   
                    if cur_diff < min_diff:
                        min_diff = cur_diff
                        target_mg = mg
                    print("stage", i, "cur_diff", cur_diff, pre_interaction_qubits, interaction_qubits)
                lg.append(target_mg)
                colored_gates.remove(target_mg) 
        return lg
    else:
            
        return colored_gates

def enola(cz_blocks, Row, n):
    list_gates = []
    for gates in cz_blocks:
        # print(cz_blocks)
        list_gates += storage_gate_scheduling(gates, False)
    qubit_mapping = place_qubit((Row, Row), n, list_gates, True)
    program_list, time_mis, time_codeGen, time_placement = route_qubit(Row, Row, n, list_gates, qubit_mapping, 'maximalis', False, True, True)
    # list_movement_duration = []
    # for instruction in program_list:    
    #     duration = instruction["duration"]
    #     if instruction["type"] == "Move":
    #             list_movement_duration.append(duration)

    cir_fidelity_2q_gate = 1
    cir_fidelity_2q_gate_for_idle = 1 
    cir_fidelity_atom_transfer = 1
    cir_fidelity_1q_gate = 1
    cir_fidelity_coherence = 1
    fidelity_2q_gate_for_idle = 1 - (1-Fidelity_2Q_Gate)/2

    num_movement_stage = 0
    
    cir_qubit_idle_time = []
    list_movement_duration = []
    list_transfer_duration = []

    for i in range(n):
        cir_qubit_idle_time.append(0)

    for instruction in program_list:
        duration = instruction["duration"]
        if instruction["type"] == "Init":
            continue
        elif instruction["type"] == "Rydberg":
            list_gates = instruction["gates"]
            list_active_qubit = [False for i in range(n)]
            if len(list_gates) == 0:
                continue
            for gate in list_gates:
                list_active_qubit[gate["q0"]] = True
                list_active_qubit[gate["q1"]] = True
            # calculate the fidelity of two-qubit gates
            cir_fidelity_2q_gate *= pow(Fidelity_2Q_Gate, len(list_gates))
            # calculate the fidelity of idle qubits affected by Rydberg laser
            cir_fidelity_2q_gate_for_idle *= pow(fidelity_2q_gate_for_idle, n - 2*len(list_gates))

        elif instruction["type"] == "Activate" or instruction["type"] == "Deactivate":
            key = ""
            if instruction["type"] == "Activate":
                key = "pickup_qs"
            else:
                key = "dropoff_qs"
            list_qubits = instruction[key]
            list_active_qubit = [False for i in range(n)]
            for qubit in list_qubits:
                list_active_qubit[qubit] = True
            # calculate the fidelity of atom transfer
            cir_fidelity_atom_transfer *= pow(Fidelity_Atom_Transfer, len(list_qubits))
            list_transfer_duration.append(duration)
            for i in range(n):
                if not list_active_qubit[i]:
                    cir_qubit_idle_time[i] += duration
        elif instruction["type"] == "Move":
            if duration > 1e-4:
                for i in range(n):
                    cir_qubit_idle_time[i] += duration
                num_movement_stage += 1
                list_movement_duration.append(duration)
        else:
            raise ValueError("Wrong instruction type")
        
    for t in cir_qubit_idle_time:
        cir_fidelity_coherence *= (1 - t/Coherence_Time)
    cir_fidelity = cir_fidelity_1q_gate * cir_fidelity_2q_gate * cir_fidelity_2q_gate_for_idle \
                        * cir_fidelity_atom_transfer * cir_fidelity_coherence 
    print("cir_qubit_idle_time", cir_qubit_idle_time)
    print("cir_fidelity_1q_gate", cir_fidelity_1q_gate)
    print("cir_fidelity_2q_gate", cir_fidelity_2q_gate)
    print("cir_fidelity_2q_gate_for_idle", cir_fidelity_2q_gate_for_idle)
    print("cir_fidelity_atom_transfer", cir_fidelity_atom_transfer)
    print("cir_fidelity_coherence", cir_fidelity_coherence)
    print("coherence_time", Coherence_Time)
    
        
    return sum(list_transfer_duration), sum(list_movement_duration), cir_fidelity, cir_fidelity_1q_gate, cir_fidelity_2q_gate, cir_fidelity_2q_gate_for_idle, cir_fidelity_atom_transfer, cir_fidelity_coherence, num_movement_stage