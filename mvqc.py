from scheduler.gate_scheduler import gate_scheduling
from placer.placer import place_qubit
import matplotlib.pyplot as plt
import networkx as nx
import math

Infinity = math.inf
X_SEP = 19
Y_SEP = 15
Storage_Y_SEP = 5
Fidelity_2Q_Gate = 0.995
Fidelity_1Q_Gate = 0.995
Fidelity_Atom_Transfer = 0.999
Coherence_Time = 1.5e6 # ms
MUS_PER_FRM = 8


def check_conflict(pos, pre_move, move, dim):
    q0 = move[0]
    q1 = move[1]
    pq0 = pre_move[0]
    pq1 = pre_move[1]
    src0 = pos[pq0][dim]
    src1 = pos[q0][dim]
    dst0 = pq1[dim]
    dst1 = q1[dim]    

    if src1 - src0 == 0:
        dir_src = 0
    else:
        dir_src = (src1 - src0) // abs(src1 - src0)
    
    if dst1 - dst0 == 0:
        dir_dst = 0
    else:
        dir_dst = (dst1 - dst0) // abs(dst1 - dst0)
    
    if dir_dst != dir_src:    
        return True
    else:
        return False

def update(pos, qubit_map, empty_space, moves, storage_in_move):
    for m in moves:
        if qubit_map.has_edge(m[0], m[1]):
            qubit_map.remove_edge(m[0], m[1])
        # empty_space[pos[m[0]]].remove(m[0])
        empty_space[pos[m[1]]].append(m[0])
        qubit_map.nodes[m[0]]['pos'] = qubit_map.nodes[m[1]]['pos']
        pos[m[0]] = pos[m[1]]

    for sq in storage_in_move.keys():
        # empty_space[pos[sq]].remove(sq)
        empty_space[storage_in_move[sq]].append(sq)
        qubit_map.nodes[sq]['pos'] = storage_in_move[sq]
        pos[sq] = storage_in_move[sq]

    return pos, qubit_map, empty_space

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

def mvqc(cz_blocks, Row, n, storage_flag):
    if not storage_flag:
        list_gates = []
        for gates in cz_blocks:
            # print(cz_blocks)
            list_gates += storage_gate_scheduling(gates, storage_flag)

    else:
        list_gates = []
        for gates in cz_blocks:
            list_gates += storage_gate_scheduling(gates, storage_flag)
    print(len(list_gates), "stages")
    qubit_mapping = place_qubit((Row, Row), n, list_gates, True)

    print(qubit_mapping)

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

    empty_space = {}
    for i in range(Row):
        for j in range(-8 * Row - 2, Row):
            empty_space[(i, j)] = []

    # draw cz_graph layout
    qubit_map = nx.Graph()
    max_y = 0
    for qk in qubit_mapping:
        if qk[1] > max_y:
            max_y = qk[1]

    for i in range(len(qubit_mapping)):
        if not storage_flag:
            qubit_pos = qubit_mapping[i]
            qubit_map.add_node(i)
            qubit_map.nodes[i]['pos'] = qubit_pos
            empty_space[qubit_pos].append(i)
        else:
            qubit_pos = qubit_mapping[i]
            qubit_map.add_node(i)
            qubit_map.nodes[i]['pos'] = (qubit_pos[0], -2 - (max_y - qubit_pos[1]))
            empty_space[qubit_map.nodes[i]['pos']].append(i)    
    print("qubit mapping", qubit_mapping)      
    for gates in cz_blocks:
        for gate in gates:
            qubit_map.add_edge(gate[0], gate[1])

    print(empty_space)
    pos = nx.get_node_attributes(qubit_map, 'pos')

    # nx.draw(qubit_map, pos = pos, node_size = 50)
    # nx.draw_networkx_labels(qubit_map, pos, labels={i: str(i) for i in qubit_map.nodes()}, font_color='black')

    s_index = 0
    if storage_flag:
        qubits_not_in_storage = []
    else:
        qubits_not_in_storage = [q for q in range(n)]

    # storage_occ = {}

    # for i in range(Row):
    #     storage_occ[i] = -2
 
    print(qubit_map.nodes(), pos)
    for mg in list_gates:
        cir_fidelity_2q_gate *= pow(Fidelity_2Q_Gate, len(mg))

        move_in_qubits = []
        move_out_qubits = []

        if storage_flag:
            interaction_qubits = []
            for m in mg:
                interaction_qubits.append(m[0])
                interaction_qubits.append(m[1])
            print(mg)
            for q in interaction_qubits:
                if q not in qubits_not_in_storage:
                    move_out_qubits.append(q)
                    qubits_not_in_storage.append(q)
            
            qubits_not_in_storage_copy = qubits_not_in_storage.copy()
            for q in qubits_not_in_storage_copy:
                if q not in interaction_qubits:
                    move_in_qubits.append(q)
                    qubits_not_in_storage.remove(q)

        def get_pos(q):
            return pos[q][1]
        
        qmg = []
        static_pos = {}
        moved_qubits = []
        redundant_qubits_to_be_moved = []
        for move in mg:
            q0 = move[0]
            q1 = move[1]
            pos_q0 = pos[q0]
            pos_q1 = pos[q1]
            
            if q0 in move_out_qubits and q1 in move_out_qubits:
                # print("count redundant0")
                qmg.append(move)
                moved_qubits.append(q0)
                redundant_qubits_to_be_moved.append(q1)
                empty_space[pos[q0]].remove(q0)
                empty_space[pos[q1]].remove(q1)
                # print('in move redundant', redundant_qubits_to_be_moved)
                
                # storage_occ[pos[q0][0]] += 1
                # storage_occ[pos[q1][0]] += 1
            elif q0 in move_out_qubits:
                # print("count redundant1")
                if pos_q1 not in static_pos.keys():
                    static_pos[pos_q1] = q1
                    qmg.append(move)
                    moved_qubits.append(q0)
                    empty_space[pos[q0]].remove(q0)
                else:
                    qmg.append(move)
                    moved_qubits.append(q0)
                    redundant_qubits_to_be_moved.append(q1)
                    empty_space[pos[q0]].remove(q0)
                    empty_space[pos[q1]].remove(q1)
                    # print('in move redundant', redundant_qubits_to_be_moved)
                
                # storage_occ[pos[q0][0]] += 1                               
            elif q1 in move_out_qubits:
                print("count redundant2")
                if pos_q0 not in static_pos.keys():
                    static_pos[pos_q0] = q0
                    qmg.append((q1, q0))
                    moved_qubits.append(q1)
                    empty_space[pos[q1]].remove(q1)
                else:
                    qmg.append((q1, q0))
                    moved_qubits.append(q1)
                    redundant_qubits_to_be_moved.append(q0)
                    empty_space[pos[q0]].remove(q0)
                    empty_space[pos[q1]].remove(q1)
                    # print('in move redundant', redundant_qubits_to_be_moved)
                
                # storage_occ[pos[q1][0]] += 1                  
            else:
                # print("count redundant3")
                if pos_q1 not in static_pos.keys():
                    static_pos[pos_q1] = q1
                    qmg.append(move)
                    moved_qubits.append(q0)
                    empty_space[pos[q0]].remove(q0)
                elif pos_q0 not in static_pos.keys():
                    static_pos[pos_q0] = q0
                    qmg.append((q1, q0))
                    moved_qubits.append(q1)
                    empty_space[pos[q1]].remove(q1)
                else:
                    qmg.append(move)
                    moved_qubits.append(q0)
                    redundant_qubits_to_be_moved.append(q1)
                    empty_space[pos[q0]].remove(q0)
                    empty_space[pos[q1]].remove(q1)
                    # print('in move redundant', redundant_qubits_to_be_moved)

        storage_in_move = {}
        # move in directly with the minimum distance
        if storage_flag:  
            move_in_qubits.sort(reverse = True, key = get_pos)
            for q in move_in_qubits:
                # pos_q = pos[q]
                # pos_x = pos_q[0]
                # pos_y = pos_q[1]
                # pos_find_flag = False
                # for r in range(4 * Row):
                #     for i in range(r):
                #         j = r - i
                #         for a in [-1, 1]:
                #             npos_x = pos_x + a * i
                #             npos_y = pos_y - j
                #             if npos_x >= 0 and npos_x < Row and npos_y >= - 2 * Row - 2 and npos_y <= storage_occ[npos_x]:
                #                 empty_space[pos[q]].remove(q)
                #                 storage_in_move[q] = (npos_x, npos_y)
                #                 storage_occ[npos_x] -= 1
                #                 pos_find_flag = True
                #                 break
                #         if pos_find_flag:
                #             break
                #     if pos_find_flag:
                #         break
                empty_space[pos[q]].remove(q)
                for y in range(-2, -8 * Row - 3, -1):
                    if len(empty_space[(pos[q][0], y)]) == 0:
                        storage_in_move[q] = (pos[q][0], y)


        if not storage_flag:
            cir_fidelity_2q_gate_for_idle *= pow(fidelity_2q_gate_for_idle, n - 2*len(mg))
        else:
            cir_fidelity_2q_gate_for_idle *= pow(fidelity_2q_gate_for_idle, len(qubits_not_in_storage) - 2*len(mg))

        print(redundant_qubits_to_be_moved)
        for p in empty_space.keys():
            placed_qubits = empty_space[p]
            for pq in placed_qubits:
                if pq not in move_in_qubits and pos[pq][1] >= 0:
                    if p not in static_pos.keys():
                        static_pos[p] = pq
                    if pq != static_pos[p] and pq not in moved_qubits and pq not in redundant_qubits_to_be_moved:
                        empty_space[pos[pq]].remove(pq)
                        redundant_qubits_to_be_moved.append(pq)
                        print('not in move redundant', redundant_qubits_to_be_moved)

        # print("redundant qubits to be moved", redundant_qubits_to_be_moved)

        rq_moved_pos = {}
        for rq in redundant_qubits_to_be_moved:
            pos_rq = pos[rq]
            pos_x = pos_rq[0]
            pos_y = pos_rq[1]
            pos_find_flag = False
            for r in range(20 * Row):
                for i in range(min(r + 1, Row)):
                    j = r - i
                    print("i, j", i, j)
                    for a in [-1, 1]:
                        for b in [-1, 1]:
                            npos_x = pos_x + a * i
                            npos_y = pos_y + b * j
                            # print("npos_x,", npos_x, "npos_y,", npos_y)
                            if npos_x >= 0 and npos_x < Row and npos_y >= 0 and npos_y < Row:
                                print("npos_x,", npos_x, "npos_y,", npos_y, "empty space", empty_space[(npos_x, npos_y)])
                            if npos_x >= 0 and npos_x < Row and npos_y >= 0 and npos_y < Row and len(empty_space[(npos_x, npos_y)]) == 0:
                                # pos[rq] = (npos_x, npos_y)
                                empty_space[(npos_x, npos_y)].append(rq)
                                # qubit_map.nodes[rq]['pos'] = pos[rq]
                                rq_moved_pos[rq] = (npos_x, npos_y)
                                pos_find_flag = True
                                
                                break
                        if pos_find_flag:
                            break

                    if pos_find_flag:
                        break
                if pos_find_flag:
                    break
            print(pos_find_flag)

                # storage_in_move[q] = (pos[q][0], storage_occ[pos[q][0]])
                # storage_occ[pos[q][0]] -= 1

        move_group = []
        # formulate qmg (q0, q1) into move_group (q, pos)
        for qm in qmg:
            if pos[qm[1]] in static_pos.keys() and qm[1] == static_pos[pos[qm[1]]]:
                move_group.append((qm[0], pos[qm[1]]))
            else:
                move_group.append((qm[0], rq_moved_pos[qm[1]]))
        
        for rq in redundant_qubits_to_be_moved:
            move_group.append((rq, rq_moved_pos[rq]))

        for sq in storage_in_move.keys():
            move_group.append((sq, storage_in_move[sq]))

        move_distance = {}
        for move in move_group:
            if move[1][1] >= 0 and pos[move[0]][1] >= 0:
                move_distance[move] = abs(move[1][0] - pos[move[0]][0]) * X_SEP + abs(move[1][1] - pos[move[0]][1]) * Y_SEP
            elif move[1][1] >= 0:
                move_distance[move] = abs(move[1][0] - pos[move[0]][0]) * X_SEP + abs(move[1][1] + 2) * Y_SEP + abs(-2 - pos[move[0]][1]) * Storage_Y_SEP
            elif pos[move[0]][1] >= 0:
                move_distance[move] = abs(move[1][0] - pos[move[0]][0]) * X_SEP + abs(pos[move[0]][1] + 2) * Y_SEP + abs(-2 - move[1][1] ) * Storage_Y_SEP
            else:
                move_distance[move] = abs(move[1][0] - pos[move[0]][0]) * X_SEP + abs(move[1][1] - pos[move[0]][1]) * Storage_Y_SEP

        def get_distance(move):
            # return conflict_graph.nodes[move]['move_distance']
            return move_distance[move]
        
        moves = move_group
        moves.sort(key = get_distance)
        print(moves)

        parallel_move_groups = []
        for move in moves:
            flag = False
            for i in range(len(parallel_move_groups)):
                pg = parallel_move_groups[i]
                in_group_flag = True
                for pre_move in pg:
                    if check_conflict(pos, pre_move, move, 0) or check_conflict(pos, pre_move, move, 1):
                        in_group_flag = False
                        break
                if in_group_flag:
                    parallel_move_groups[i].append(move)
                    flag = True
                    break
            
            if not flag:
                parallel_move_groups.append([move])

        for ms in parallel_move_groups:
            num_movement_stage += 1
            list_active_qubits = []
            for m in ms:
                list_active_qubits.append(m[0])
                if m[0] in move_in_qubits:
                    move_in_qubits.remove(m[0])
                if m[0] in move_out_qubits:
                    move_out_qubits.remove(m[0])
            cir_fidelity_atom_transfer *= pow(Fidelity_Atom_Transfer, len(list_active_qubits))
            for i in range(n):
                if i not in list_active_qubits and ((i in qubits_not_in_storage and i not in move_out_qubits) or i in move_in_qubits):
                    cir_qubit_idle_time[i] = cir_qubit_idle_time[i] + MUS_PER_FRM * 2

            ms.sort(reverse = True, key = get_distance)
            move_duration = 200*((get_distance(ms[0]) /110)**(1/2))
            for i in range(n):
                if (i in qubits_not_in_storage and i not in move_out_qubits) or i in move_in_qubits:
                    cir_qubit_idle_time[i] += move_duration
            list_transfer_duration.append(2 * MUS_PER_FRM)
            list_movement_duration.append(move_duration)
            print("move in qubits", move_in_qubits)
            print("move out qubits", move_out_qubits)
        print("one stage finished")

        # parallel_move_groups.sort(reverse = True, key = len)
        print("move steps", len(parallel_move_groups))
        # for selective_move_group in parallel_move_groups:

        for rq in rq_moved_pos.keys():
            # empty_space[pos[rq]].remove(rq)
            pos[rq] = rq_moved_pos[rq]
            # empty_space[pos[rq]].append(rq)
            qubit_map.nodes[rq]['pos'] = pos[rq]
            
        pos, qubit_map, empty_space = update(pos, qubit_map, empty_space, qmg, storage_in_move)

        print("empty space")
        for p in empty_space.keys():
            if len(empty_space[p]):
                print(p, empty_space[p])
        
        # plt.figure(s_index)
        # plt.xlim(-1, Row)
        # plt.ylim(- 2 * Row - 2, Row)
        # plt.gca().set_aspect('equal', adjustable='box')
        # pos = nx.get_node_attributes(qubit_map, 'pos')
        # nx.draw(qubit_map, pos = pos, node_size = 50)
        # nx.draw_networkx_labels(qubit_map, pos, labels={i: str(i) for i in qubit_map.nodes()}, font_color='black')
        s_index += 1

        index = 0
        for p in empty_space.keys():
            index += len(empty_space[p])
        print("index", index)
        pos_redundant_graph = nx.Graph()
        for p in empty_space.keys():
            pos_qubits = list(empty_space[p])
            for q in pos_qubits:
                for m in qmg:
                    if q == m[0]:
                        pos_qubits.remove(q)
                        pos_qubits.remove(m[1])
                        break
                    elif q == m[1]:
                        pos_qubits.remove(q)
                        pos_qubits.remove(m[0])
                        break
            if len(pos_qubits):
                print(pos_qubits)
                pos_redundant_graph.add_node(str(pos_qubits))
                pos_redundant_graph.nodes[str(pos_qubits)]['pos'] = p

        print(qubit_map.nodes(), pos)
        # plt.figure(s_index)
        # plt.xlim(-1, Row)
        # plt.ylim(- 2 * Row - 2, Row)
        # plt.gca().set_aspect('equal', adjustable='box')
        # p = nx.get_node_attributes(pos_redundant_graph, 'pos')
        # nx.draw(pos_redundant_graph, pos = p, node_size = 50)   
        # nx.draw_networkx_labels(pos_redundant_graph, p, labels={i: str(i) for i in pos_redundant_graph.nodes()}, font_color='black')
        
        s_index += 1

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