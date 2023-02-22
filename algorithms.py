import random
import math


def kruskal(nodes, distances):
    subset = {}
    k = 0
    for node in nodes:
        subset[node] = k
        k += 1

    tree = []
    for edge in sorted(distances, key=distances.get):
        #print(edge)
        #print(str(subset[edge[0]]) + str(subset[edge[1]]))
        #print(subset)
        if subset[edge[0]] != subset[edge[1]]:           
            tree.append(edge)
            rep_set = subset[edge[0]]
            for node in subset:
                if subset[node] == rep_set:
                    subset[node] = subset[edge[1]]

    return tree


def steiner_heuristic(nodes, n_nodes, distances):
    f_nodes = nodes + n_nodes

    shortest_distances = {}
    paths = {} 
    for i in f_nodes:
        for j in f_nodes:
            if i == j:
                shortest_distances[(i,j)] = 0
                paths[(i,j)] = {}
            elif (i,j) in distances:
                shortest_distances[(i,j)] = distances[(i,j)]
                paths[(i,j)] = {(i,j)}
            elif (j,i) in distances:
                shortest_distances[(i,j)] = distances[(j,i)]
                shortest_distances[(j,i)] = distances[(j,i)]
                paths[(i,j)] = {(i,j)}
                paths[(j,i)] = {(j,i)}
            else:
                shortest_distances[(i,j)] = math.inf

    for k in f_nodes:
        for i in f_nodes:
            for j in f_nodes:
                if (shortest_distances[(i,j)] > 
                    shortest_distances[(i,k)] + shortest_distances[(k,j)]):

                    shortest_distances[(i,j)] = (shortest_distances[(i,k)] 
                                                + shortest_distances[(k,j)])
                    shortest_distances[(j,i)] = (shortest_distances[(i,k)] 
                                                + shortest_distances[(k,j)])
                    paths[(i,j)] = paths[(i,k)] | paths[(k,j)]
                    paths[(j,i)] = paths[(i,k)] | paths[(k,j)]

    for edge in list(shortest_distances):
        if (shortest_distances[edge] == math.inf or 
            (edge[0] not in nodes) or (edge[1] not in nodes)):

            del shortest_distances[edge]

    tree = kruskal(nodes, shortest_distances)

    for edge in tree:
        if edge not in distances:
            tree.remove(edge)
            for path_component in paths[edge]:
                if path_component[0] < path_component[1]:
                    tree.append(path_component)
                elif path_component[1] < path_component[0]:
                    tree.append((path_component[1], path_component[0]))

    return tree


def cover_heuristic(nodes, edges):
    selected_nodes = []

    while edges:
        edge = random.choice(edges)
        edges.remove(edge)

        for i in [0,1]:
            removed_edges = []
            for neighbor_edge in edges:   
                if neighbor_edge[0] == edge[i] or neighbor_edge[1] == edge[i]:
                    removed_edges.append(neighbor_edge)
            if i == 0 or removed_edges:
                selected_nodes.append(edge[i])
            edges = list(set(edges) - set(removed_edges))
    
    return selected_nodes
                

def cover_heuristic_2(nodes, edges):
    node_neighbors = {}
    for i in nodes:
        neighbors = 0
        for edge in edges:
            if edge[0] == i or edge[1] == i:
                neighbors += 1
        node_neighbors[i] = neighbors

    selected_nodes = []
    while node_neighbors:
        node = max(node_neighbors, key=node_neighbors.get)
        selected_nodes.append(node)
        node_neighbors.pop(node)

        for edge in edges:
            if edge[0] == node:
                node_neighbors.pop(edge[1], None)
                for edge2 in edges:
                    if edge2[0] in node_neighbors and edge2[1] == edge[1]:
                        node_neighbors[edge2[0]] -= 1
                    elif edge2[1] in node_neighbors and edge2[0] == edge[1]:
                        node_neighbors[edge2[1]] -= 1
            elif edge[1] == node:
                node_neighbors.pop(edge[0], None)
                for edge2 in edges:
                    if edge2[0] in node_neighbors and edge2[1] == edge[0]:
                        node_neighbors[edge2[0]] -= 1
                    elif edge2[1] in node_neighbors and edge2[0] == edge[0]:
                        node_neighbors[edge2[1]] -= 1

    print("sel. nodes" + str(selected_nodes))
    
    return selected_nodes