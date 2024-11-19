    # print(move_group)

    # conflict_graph = nx.Graph()
    # for move in move_group:
    #     pre_moves = list(conflict_graph.nodes())
    #     conflict_graph.add_node(move)

    #     conflict_graph.nodes[move]['move_distance'] = abs(pos[move[1]][0] - pos[move[0]][0]) + abs(pos[move[1]][1] - pos[move[0]][1])

    #     for pre_move in pre_moves:
    #         if check_conflict(pos, pre_move, move, 0) or check_conflict(pos, pre_move, move, 1):
    #             conflict_graph.add_edge(pre_move, move)

    # plt.figure(s_index)
    # nx.draw(conflict_graph, node_size = 50)


    # static_pos = {}
    # moved_qubits = []
    # move_group = []
    # other_qubits_to_be_moved = []
    # for move in mg:
    #     q0 = move[0]
    #     q1 = move[1]
    #     if pos[q1] not in static_pos.keys():
    #         static_pos[pos[q1]] = q1
    #         move_group.append(move)
    #         moved_qubits.append(move[0])
    #     elif pos[q0] not in static_pos.keys():
    #         static_pos[pos[q0]] = q0
    #         move_group.append((move[1], move[0]))
    #         moved_qubits.append(move[1])
    #     else:
    #         moved_qubits.append(move[0])
    #         move_group.append(move)
    #         other_qubits_to_be_moved.append(move[1])
    
    # for p in empty_space.keys():
    #     for q in empty_space[p]:
    #         if p not in static_pos.keys():
    #             static_pos[p] = q
    #         if q != static_pos[p] and q not in moved_qubits and q not in other_qubits_to_be_moved:
    #             other_qubits_to_be_moved.append(q)

    # print("other qubits to be moved", other_qubits_to_be_moved)
    # flag = False
    # for om in other_qubits_to_be_moved:
    #     pos_om = pos[om]
    #     for i in range(Row):
    #         for j in range(Row):
    #             for a in [-1, 1]:
    #                 for b in [-1, 1]:
    #                     if pos_om[0] + a * i < 0 or pos_om[0] + a * i >= Row:
    #                         continue
    #                     if pos_om[1] + b * j < 0 or pos_om[1] + b * j >= Row:
    #                         continue                        
    #                     if len(empty_space[(pos_om[0] + a * i, pos_om[1] + b * j)]) == 0:
    #                         empty_space[pos_om].remove(om)
    #                         empty_space[(pos_om[0] + a * i, pos_om[1] + b * j)].append(om)
    #                         pos[om] = (pos_om[0] + a * i, pos_om[1] + b * j)
    #                         qubit_map.nodes[om]['pos'] = (pos_om[0] + a * i, pos_om[1] + b * j)
    #                         flag = True
    #                         break
    #                 if flag:
    #                     break
    #             if flag:
    #                 break
    #         if flag:
    #             break
    #     print("move flag", flag)


    # index = 0
    # for p in empty_space.keys():
    #     index += len(empty_space[p])
    # print("idnex", index)
    # pos_redundant_graph = nx.Graph()
    # for p in empty_space.keys():
    #     pos_qubits = list(empty_space[p])
    #     for q in pos_qubits:
    #         for m in move_group:
    #             if q == m[0]:
    #                 pos_qubits.remove(q)
    #                 pos_qubits.remove(m[1])
    #                 break
    #             elif q == m[1]:
    #                 pos_qubits.remove(q)
    #                 pos_qubits.remove(m[0])
    #                 break
    #     if len(pos_qubits):
    #         print(pos_qubits)
    #         pos_redundant_graph.add_node(str(pos_qubits))
    #         pos_redundant_graph.nodes[str(pos_qubits)]['pos'] = p
    
    # plt.figure(s_index)
    # plt.xlim(-1, Row)
    # plt.ylim(-1, Row)
    # plt.gca().set_aspect('equal', adjustable='box')
    # p = nx.get_node_attributes(pos_redundant_graph, 'pos')
    # nx.draw(pos_redundant_graph, pos = p, node_size = 50)   
    # nx.draw_networkx_labels(pos_redundant_graph, p, labels={i: str(i) for i in pos_redundant_graph.nodes()}, font_color='black')
    
    # s_index += 1