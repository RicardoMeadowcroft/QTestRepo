import matrices
import models

#print(matrices.minimum_spanning_tree([1,2,3,4], {(1,2): 2, (2,3): 4, (3,4): 6, (2,4): 13}, 1).todense())
#print(matrices.minimum_spanning_tree([1,2,3,4], {(1,2): 2, (2,3): 4, (3,4): 6, (2,4): 13, (1,3): 12, (1,4): 22}, 1).todense())
#print(matrices.minimum_spanning_tree([1,2,3,4,5, 6], {(1,2): 2, (2,3):4, (3,4): 6, (2,3): 13, (4,5): 8, (1,3): 12, (5,6): 9}, 1).todense())

#print(matrices.vertex_cover([1,2,3,4,5,0], {(1,2), (2,3), (3,4), (2,3), (4,5), (1,3), (5,0)}, 10).todense())

print(matrices.set_cover([0,1,2,3,4,5], {(0,1), (0,2), (0,3), (2,3),(0,4),(4,5)}, 2).todense())

models.set_cover([0,1,2,3,4,5], {(0,1), (0,2), (0,3), (2,3),(0,4),(4,5)}, 2)


