from timeit import repeat

from concept_formation.trestle import TrestleTree
from concept_formation.datasets import load_rb_s_07
from concept_formation.structure_mapper import structure_map, structurizeJSON
from concept_formation.utils import mean


tree = TrestleTree()
#data = load_rb_s_07()

#print('initialization done')

#def test():
#    print()
#    print("RESET")
#    print()
#    tree.clear()
#    tree.fit(data[0:100], randomize_first=False)
#
##test()
#print(mean(repeat(test, number=1)))

x = {'c1': {'a': 'v0'},
     'c2': {'a': 'v0'},
     'c3': {'a': 'v0'},
     'r1': ['<', 'c1.a', 'c2.a'],
     'r2': ['<', 'c2.a', 'c3.a']}

y = {'c1': {'a': 'v1'},
     'c2': {'a': 'v2'},
     'c3': {'a': 'v3'},
     'r1': ['<', 'c2.a', 'c3.a']}

action = {'v1': {'value': 5}, 
          'v2': {'value': 3}, 
          'op1': ['multiply', 'v1.value', 'v2.value', 'op1-output.value'],
          'op1-output': {'value': 25}, 
          'op2': ['add', 'v2.value', 'op1-output.value', 'op2-output.value'],
          'op2-output': {'value': 28}}

action2 = {'v1': {'value': 20}, 
           'v2': {'value': 10}, 
           'op1': ['multiply', 'v1.value', 'v2.value', 'op1-output.value'],
           'op1-output': {'value': 200}, 
           'op2': ['add', 'v2.value', 'op1-output.value', 'op2-output.value'],
           'op2-output': {'value': 210}}

tree.ifit(action)
tree.ifit(action2)
print(tree)
#print(structure_map(tree.root, action2))
