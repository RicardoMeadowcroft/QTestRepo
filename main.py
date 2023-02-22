import random

import mappers as m

X_MIN = 19.2792
X_MAX = 19.6908
Y_MIN = -99.2806
Y_MAX = -98.8376

DEFAULT_COORDS = (19.3446,-99.1996)
DEFAULT_RANGE = (0.06, 0.08)

def parse_coords(coords):
    try:
        coords = coords.split(',')
        if len(coords) == 2:
            coords = (float(coords[0]), float(coords[1]))
            inputed = True     
        else:
            print("Write two coordinates")
            inputed = False
    except ValueError:
            print("Write decimal values")
            inputed = False
        
    return [inputed, coords]

print("Input to select your operation mode:\n"+
        "\t1: Minimum Spanning Tree \n"+
        "\t2: Steiner Tree \n"+
        "\t3: Minimum Vertex Cover \n"+
        "\t4: Minimum Set Cover")
mode_select = None
while mode_select not in ['1','2','3','4']:
    mode_select = input()
    if mode_select not in ['1','2','3','4']:
        print("Write an integer 1-4")

print("Input to how to input coordinates:\n"+
        "\t1: Manual \n"+
        "\t2: Random locations in region \n"+
        "\t3: Random locations & region \n"+
        "\t4: Default location")
random_select = None
while random_select not in ["1","2","3","4"]:
    random_select = input()
    if random_select not in ["1","2","3","4"]:
        print("Write an integer 1-4")

if random_select in ['1','2']:
    inputed = False
    print("Input the central coordinates, with x and y coordinates separated by commas")
    while not inputed:
        [inputed, area_coords] = parse_coords(input())
elif random_select == '3':
    area_coords = [random.uniform(X_MIN,X_MAX), random.uniform(Y_MIN,Y_MAX)]
else:
    area_coords = DEFAULT_COORDS   

if random_select in ['1','2']:
    inputed = False
    print("Input the range (in degrees) of the x and y axis (d for default)")
    while not inputed:    
        coord_range = input()
        if coord_range == 'd':
            coord_range = DEFAULT_RANGE
            inputed = True
        else:
            [inputed, coord_range] = parse_coords(coord_range)
elif random_select == '3':
    scale = random.uniform(0.2,5)
    coord_range = [scale*DEFAULT_RANGE[0], scale*DEFAULT_RANGE[1]]
else:
    coord_range = DEFAULT_RANGE

area_min = (area_coords[0] - coord_range[0]/2, area_coords[1] - coord_range[1]/2)
area_max = (area_coords[0] + coord_range[0]/2, area_coords[1] + coord_range[1]/2)

if mode_select != '2':
    if random_select == '1':
        print("Input coordinates (x, y separated by comma, locations separated with enter), " 
              "write 'e' to end")
        coord_list = []
        ended = False
        while not ended:
            coords = input()
            if coords == 'e':
                ended = True
            else:
                [inputed, coords] = parse_coords(coords)
                if inputed:
                    if ((area_min[0] < coords[0] < area_max[0]) 
                        and (area_min[1] < coords[1] < area_max[1])): 

                        coord_list.append(coords)
                    else:
                        print("Input a coordinate in range")
    else:
        print("Input number of locations")
        inputed = False
        while not inputed:
            number = input()
            try:
                number = int(number)
                inputed = True
            except TypeError:
                print("Input a number")

        coord_list = []
        for i in range(number):
            coord_list.append((random.uniform(area_min[0],area_max[0]), 
                               random.uniform(area_min[1],area_max[1])))
else:
    if random_select == '1':
        print("Input terminal coordinates (x, y separated by comma, locations separated "
              "with enter), write 'e' to end")
        coord_list = []
        ended = False
        while not ended:
            coords = input()
            if coords == 'e':
                ended = True
            else:
                [inputed, coords] = parse_coords(coords)
                if inputed:
                    if ((area_min[0] < area_coords[0] < area_max[0])
                        and (area_min[1] < area_coords[1] < area_max[1])): 
                        
                        coord_list.append(coords)
                    else:
                        "Input a coordinate in range"
        print("Input non-terminal coordinates (x, y separated by comma, locations separated with "
              "enter), write 'e' to end")
        n_coord_list = []
        ended = False
        while not ended:
            coords = input()
            if coords == 'e':
                ended = True
            else:
                [inputed, coords] = parse_coords(coords)
                if inputed:
                    if ((area_min[0] < area_coords[0] < area_max[0]) 
                        and (area_min[1] < area_coords[1] < area_max[1])): 
                        
                        n_coord_list.append(coords)
                    else:
                        print("Input a coordinate in range")
    else:
        print("Input number of terminal locations")
        inputed = False
        while not inputed:
            number = input()
            try:
                number = int(number)
                inputed = True
            except TypeError:
                print("Input a number")

        coord_list = []
        for i in range(number):
            coord_list.append((random.uniform(area_min[0],area_max[0]), 
                               random.uniform(area_min[1],area_max[1]))) 

        print("Input number of non-terminal locations")
        inputed = False
        while not inputed:
            number = input()
            try:
                number = int(number)
                inputed = True
            except TypeError:
                print("Input a number")

        n_coord_list = []
        for i in range(number):
            n_coord_list.append([random.uniform(area_min[0],area_max[0]), 
                                 random.uniform(area_min[1],area_max[1])]) 


print("Input maximum adjacency distance (in km)")
inputed = False
while not inputed:
    max_dist = input()
    try:
        max_dist = float(max_dist)*1000
        inputed = True
    except TypeError:
        print("Input a decimal number")


print("Input to select algorithm 1, 2 or 3:")
algo_select = None
while algo_select not in ['1','2','3']:
    algo_select = input()
    if algo_select not in ['1','2','3']:
        print("Write an integer 1-3")

if mode_select == '1':
    m.map_ms_tree(area_min, area_max, coord_list, max_dist, algo_select)
elif mode_select == '2':
    m.map_steiner_tree(area_min, area_max, coord_list, n_coord_list, max_dist, algo_select)
elif mode_select == '3':
    m.map_vertex_cover(area_min, area_max, coord_list, max_dist, algo_select)
else:
    m.map_set_cover(area_min, area_max, coord_list, max_dist, algo_select)


        









