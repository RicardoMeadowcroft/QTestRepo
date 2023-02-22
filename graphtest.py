import algorithms as a
import matrices as m

#test_nodes = [0,1,2,3]
#test_dict = {(0,1):22, (0,2):122, (0,3):2, (1,2):23, (1,3):100, (2,3):25}
#print(test_dict)
#print(a.kruskal(test_nodes, test_dict))
#print(m.minimum_spanning_tree(test_nodes,test_dict,100))

test_nodes = [0,1,2,3]
test_list = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
print(test_list)
print(a.cover_heuristic(test_nodes, test_list))