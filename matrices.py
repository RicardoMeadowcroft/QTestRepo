from itertools import combinations
from xml.etree.ElementTree import tostring
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
    A = dok_matrix((len(nodes), len(nodes)))
    for node in nodes:
        A[node,node] = 1
    for edge in edges: 
        A[edge[0],edge[1]] = w
        A[edge[0],edge[0]] -= w
        A[edge[1],edge[1]] -= w
        #A[edge[1],edge[0]] = w

    
    return A


#Reformulate these to directly use the model

def set_cover (nodes, edges, w):

    m = len(nodes)
    for i in nodes:
        d = 0
        for edge in edges:
            if (edge[0] == i or edge[1] == i):
                d += 1
        m += d.bit_length()
    
    A = dok_matrix((m, m))
    
    c = len(nodes)

    for i in nodes:

        A[i,i] += 1 - w 

        d = 0
        for edge in edges:
            if (edge[0] == i or edge[1] == i):
                j = edge[1] if edge[0]==i else edge[0]
                d += 1
                
                A[j,j] -= 2*w
                A[i,j] += w
                A[j,i] += w

                for edge2 in edges:
                    if (edge2[0] == i or edge2[1] == i):
                        k = edge2[1] if edge2[0]==i else edge2[0]

                        A[j,k] += w/2
                        A[k,j] += w/2

        
        for j in range(d.bit_length()):
            A[c+j,c+j] += 2**(j+1)*w
            A[i,c+j] -= 2**j*w
            A[c+j,i] -= 2**j*w

            for edge in edges:
                if (edge[0] == i or edge[1] == i):
                    k = edge[1] if edge[0]==i else edge[0]

                    A[k,c+j] -= 2**(j)*w
                    A[c+j,k] -= 2**(j)*w

            for k in range(d.bit_length()):
                A[c+j,c+k] += 2**(j+k-1)*w
                A[c+k,c+j] += 2**(j+k-1)*w
            

        c += d.bit_length()

    return A
