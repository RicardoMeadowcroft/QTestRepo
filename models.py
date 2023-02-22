from itertools import combinations
from xml.etree.ElementTree import tostring
import dimod
from scipy.sparse import dok_matrix


def minimum_spanning_tree (nodes, distances, w):
    variables = list(distances.keys())
    
    n = len(nodes)

    for i in range (3,n):
        for subset in combinations(nodes, i):
            empty = True
            for edge in combinations(subset,2):
                if edge in distances:
                    empty = False
            if not empty:
                for j in range (0, (i-1).bit_length()):
                    variables.append((subset,j))

    A = dok_matrix((len(variables), len(variables)))
    
    for i in range(len(variables)):
        for j in range(i,len(variables)):
            if j < len(distances):
                if i == j:
                    A[i,j] = distances[variables[i]] + w*(n - 2 - 2**(n-1)*(n-2))
                else:
                    (a,b) = variables[i]
                    (c,d) = variables[j]
                    if a==c or a==d or b==c or b==d:
                        A[i,j] = w*2**(n-2)
                    else:
                        A[i,j] = w*2**(n-3)              
            else:
                if i < len(distances):
                    if set(variables[i]).issubset(variables[j][0]):
                        A[i,j] = w*2**(variables[j][1]+1)
                else:
                    if i == j:
                        A[i,j] = w*2**(variables[j][1])*(2**(variables[j][1])
                                 -2*len(variables[j][0])+2)
                    elif variables[i][0] == variables[j][0]:
                        A[i,j] = w*2**(variables[i][1]+variables[j][1]+1)


    return (A+A.transpose)/2


def vertex_cover (nodes, edges, w):
    linear = {}
    quadratic = {}
    for node in nodes:
        linear[str(node)] = 1
    for edge in edges: 
        (i,j) = (edge[0],edge[1]) if edge[0] < edge[1] else (edge[1],edge[0])
        quadratic[(str(i),str(j))]  = 2*w
        linear[str(i)] -= w
        # are we missing linear[str(j)] -= w? check

    vartype = dimod.BINARY
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, vartype)

    return bqm


#Reformulate these to directly use the model

def set_cover (nodes, edges, w):
    linear = {}
    quadratic = {}

    for i in nodes:

        linear[str(i)] = linear.setdefault(str(i),0) + 1 - w 

        d = 0
        for edge in edges:
            if (edge[0] == i or edge[1] == i):
                j = edge[1] if edge[0]==i else edge[0]
                d += 1
                
                linear[str(j)] = linear.setdefault(str(j),0) - 2*w

                if (i<j): 
                    quadratic[(str(i),str(j))] = quadratic.setdefault((str(i),str(j)),0) + 2*w
                else:
                    quadratic[(str(j),str(i))] = quadratic.setdefault((str(j),str(i)),0) + 2*w

                for edge2 in edges:
                    if (edge2[0] == i or edge2[1] == i):
                        k = edge2[1] if edge2[0]==i else edge2[0]

                        if (j<k): 
                            quadratic[(str(j),str(k))] = quadratic.setdefault((str(j),str(k)),0) + w
                        elif (k<j):
                            quadratic[(str(k),str(j))] = quadratic.setdefault((str(k),str(j)),0) + w
                        else:
                            linear[str(j)] = linear.setdefault(str(j),0) + w

        
        for j in range(d.bit_length()):
            linear["o"+str(i)+"s"+str(j)] = 2**(j+1)*w + 2**(2*j)*w
            quadratic[(str(i),"o"+str(i)+"s"+str(j))] = -2**(j+1)*w

            for edge in edges:
                if (edge[0] == i or edge[1] == i):
                    k = edge[1] if edge[0]==i else edge[0]

                    quadratic[(str(k),"o"+str(i)+"s"+str(j))] = -2**(j+1)*w

            for k in range(j+1,d.bit_length()):
                quadratic[("o"+str(i)+"s"+str(j),"o"+str(i)+"s"+str(k))] = 2**(j+k+1)*w #Is this j+k or j+k+1? Double check

    vartype = dimod.BINARY
    bqm = dimod.BinaryQuadraticModel(linear, quadratic, vartype)

    return bqm
