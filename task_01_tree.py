import random 

class Node():

    def __init__(self, ind, value):
        self.id = ind
        self.val = value

class Tree():
    def __init__(self):
        # генерируем дерево вида 
        # {node_id: {'node': node_obj, 'link': [childs node_id,...,...]}}

        self.tree = dict()    
        self.root_id = 0        
        _nd = Node(self.root_id, 'root')
        self.tree[self.root_id] = {'node': _nd, 'links': []}
        self.nodes = 1

    def addChilds(self, parent_id, values = []):
        child_nodes = [Node(i[0],i[1]) for i in zip(range(self.nodes, self.nodes+len(values)), values)]
        self.nodes += len(values)
        child_id = []
        for nd in child_nodes:
            self.tree[nd.id] = {'node': nd, 'links': [parent_id]}
            child_id.append(nd.id)
        
        self.tree[parent_id]['links'] += [nd.id for nd in child_nodes]
        return child_id
    
    def createRandomTree(self, prob, parents = [], level = 0):

        if level == 0:
            parents = [self.root_id]
            
        for p in parents:
            if (random.random()<prob) or (level<=2):  ## делаем обязательным создание первх двух уровней, дальше полагаемся на вероятность

                qty = random.randint(1,2)
                add_nodes = [('val_'+str(random.randint(1,100))) for i in range(qty)]
                _parent = self.addChilds(p, add_nodes)
  
                self.createRandomTree(prob, _parent, level +1)
                
    def getTreeValue(self):
        # возвращает дерево вида: 
        #{node_id: {'node': node.val, 'link': [childs node_id,...,...]}}
        
        return {k: {'node': self.tree[k]['node'].val, 'links': self.tree[k]['links']} for k in self.tree.keys()}

    
    def getTree(self):
        # возвращает дерево вида:
        #{node_id: {'node': node_obj, 'link': [childs node_id,...,...]}}
        
        return self.tree
      
      
def displayTreeRecursive(nodes = [], level = 0):
    if level ==0:
        nodes = tree_dict[0]['links']
        print(tree_dict[0]['node'].val)
   
    for n in nodes:

        print(f'-{"--"*level*2}',f"{tree_dict[n]['node'].id}: {tree_dict[n]['node'].val}")
        displayTreeRecursive(tree_dict[n]['links'][1:], level +1)
    
def exploreTreeLoop():
    tree = [0] + tree_dict[0]['links']
    pos = 0
    while pos < len(tree_dict.keys()):

        # do something with nodes
        print(f"Processing node: {tree[pos]}:{tree_dict[pos]['node'].val}")   

        links = tree_dict[tree[pos]]['links'][1:]
        if len(links) >0:
            tree += links
        pos +=1
        
        
        
t = Tree()
t.createRandomTree(0.5)
print(f'\ncreated tree with {len(t.getTree().keys())} nodes')

import pprint

tree_dict = t.getTree()

print('\n1. Show tree with node objects')
print('Tree model:')
print("     {node_id: {'node': node_obj, 'link': [childs node_id,...,...]}}\n")
pprint.pprint(tree_dict)

print('\n2. Show tree with node values:')
print('Tree model:')
print("     {node_id: {'node': node.val, 'link': [childs node_id,...,...]}}\n")
pprint.pprint(t.getTreeValue())

print('\n3. Explore tree with recurion\n')
displayTreeRecursive()

print('\n4. Explore tree with loop\n')
exploreTreeLoop()