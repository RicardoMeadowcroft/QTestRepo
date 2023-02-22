import math
import random
import test_mapper as tm

X_MIN = 19.2792
X_MAX = 19.6908
Y_MIN = -99.2806
Y_MAX = -98.8376

DEFAULT_RANGE = (0.06, 0.08)
DEFAULT_DIST = 2

DEFAULT_NEIGHBORS = 4

DEFAULT_WEIGHT = 600

print("Input to select graph used:\n"+
        "\t1: Random Street Map \n"+
        "\t2: Random Graph")
graph_select = None
while graph_select not in ['1','2']:
    graph_select = input()
    if graph_select not in ['1','2']:
        print("Write the integer 1 or 2")

print("Input to select problem:\n"+
        "\t1: Set Cover \n"+
        "\t2: Vertex Cover")
prob_select = None
while prob_select not in ['1','2']:
    prob_select = input()
    if prob_select not in ['1','2']:
        print("Write the integer 1 or 2")      

print("Input to select algorithm used:\n"+
        "\t1: Heuristic \n"+
        "\t2: Quantum")
algo_select = None
while algo_select not in ['1','2']:
    algo_select = input()
    if algo_select not in ['1','2']:
        print("Write the integer 1 or 2")

print("Input number of nodes") 
inputed = False
while not inputed:
    nodes = input()
    try:
        nodes = int(nodes)
        inputed = True
    except TypeError:
        print("Input a number")

print("Input number of repetitions") 
inputed = False
while not inputed:
    reps = input()
    try:
        reps = int(reps)
        inputed = True
    except TypeError:
        print("Input a number")

if graph_select=="1":
    node_num = []
    runtime = []
    for i in range(reps):
        is_last = (i == len(reps)-1)

        area_coords = [random.uniform(X_MIN,X_MAX), random.uniform(Y_MIN,Y_MAX)]

        scale = random.uniform(0.2,5)
        coord_range = [scale*DEFAULT_RANGE[0], scale*DEFAULT_RANGE[1]]

        area_min = (area_coords[0] - coord_range[0]/2, area_coords[1] - coord_range[1]/2)
        area_max = (area_coords[0] + coord_range[0]/2, area_coords[1] + coord_range[1]/2)

        max_dist = scale*DEFAULT_DIST*5000/math.sqrt(nodes)

        coord_list = []
        for j in range(nodes):
            coord_list.append((random.uniform(area_min[0],area_max[0]), 
                               random.uniform(area_min[1],area_max[1])))

        print(area_min)
        print(area_max)
        print(coord_list)
        print(max_dist)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~+++")

        res= tm.map_set_cover(area_min, area_max, coord_list, max_dist, algo_select, prob_select, is_last, DEFAULT_WEIGHT)
        node_num.append(res[0])
        runtime.append(res[1])

    print("Avg Runtime: " + str(sum(runtime)/len(runtime)) + "\n" +
            "Avg #Nodes: " + str(sum(node_num)/len(node_num)))


else:
    node_num = []
    runtime = []
    for i in range(reps):
        edge_prob = DEFAULT_NEIGHBORS / nodes

        res= tm.graph_set_cover(nodes, edge_prob, algo_select, prob_select, DEFAULT_WEIGHT)
        node_num.append(res[0])
        runtime.append(res[1])

    print("Avg Runtime: " + str(sum(runtime)/len(runtime)) + "\n" +
            "Avg #Nodes: " + str(sum(node_num)/len(node_num)))
    
    

        
