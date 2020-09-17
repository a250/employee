import pprint
import random


class Node:
    def __init__(self, ind, value):
        self.id = ind
        self.val = value


class Tree:
    def __init__(self):
        """
        Create 'tree' with single 'root' node

        'tree' structure: {node_id: {'node': node_obj, 'link': [childs node_id,...,...]}}
        """

        self.tree = dict()
        self.root_id = 0
        _nd = Node(self.root_id, "root")
        self.tree[self.root_id] = {"node": _nd, "links": []}
        self.nodes = 1

    def addChilds(self, parent_id, values=[]):
        child_nodes = [
            Node(i[0], i[1])
            for i in zip(range(self.nodes, self.nodes + len(values)), values)
        ]
        self.nodes += len(values)
        child_id = []
        for nd in child_nodes:
            self.tree[nd.id] = {"node": nd, "links": [parent_id]}
            child_id.append(nd.id)

        self.tree[parent_id]["links"] += [nd.id for nd in child_nodes]
        return child_id

    def createRandomTree(self, prob, parents=[], level=0):
        """
        Create random 'tree' with at least 2 levels of nodes

        """

        if level == 0:
            parents = [self.root_id]

        for p in parents:
            if (random.random() < prob) or (level <= 2):

                qty = random.randint(1, 2)
                add_nodes = [("val_" + str(random.randint(1, 100))) for i in range(qty)]
                childs_list = self.addChilds(p, add_nodes)

                self.createRandomTree(prob, childs_list, level + 1)

    def getTreeValue(self):
        """
        return tree in dict object:

        {node_id: {'node': node.val, 'link': [childs node_id,...,...]}}
        """

        return {
            k: {"node": self.tree[k]["node"].val, "links": self.tree[k]["links"]}
            for k in self.tree.keys()
        }

    def getTree(self):
        """
        return tree in dict object:

        {node_id: {'node': node_obj, 'link': [childs node_id,...,...]}}
        """
        return self.tree


def exploreTreeRecursive(func, nodes=[], level=0):
    """
    Move through tree recursively.
    Required tree_dict variable.


    Arguments:
     func -- would be call on every node, func(node, level)

    """
    if level == 0:
        nodes = tree_dict[0]["links"]
        node = tree_dict[0]["node"]
        if func:
            func(node, level)

    for n in nodes:
        if func:
            func(tree_dict[n]["node"], level)
        exploreTreeRecursive(func, tree_dict[n]["links"][1:], level + 1)


def exploreTreeLoop(func):
    """
    Move through tree by loop.
    Required tree_dict variable.


    Arguments:
     func -- would be call on every node, func(node)

    """

    tree = [0] + tree_dict[0]["links"]
    pos = 0

    while pos < len(tree_dict.keys()):

        if func:
            func(tree_dict[tree[pos]]["node"])

        links = tree_dict[tree[pos]]["links"][1:]
        if len(links) > 0:
            tree += links
        pos += 1


def printNodes(node, level=None):
    """
    Output nodes with or without levels

    """
    output = f"{node.id}: {node.val}"  # pattern

    if level:
        output = f'-{"--"*level*2}' + output  # add offsets for levels
    print(output)


t = Tree()
t.createRandomTree(0.5)
print(f"\ncreated tree with {len(t.getTree().keys())} nodes")


if __name__ == "__main__":
    tree_dict = t.getTree()

    print("\n1. Tree example (Show tree with node objects): \n")
    pprint.pprint(tree_dict)

    print("\n2. Tree example (Show tree with node values): \n")
    pprint.pprint(t.getTreeValue())

    print("\nExplore tree with recurion\n")
    exploreTreeRecursive(printNodes)

    print("\nExplore tree with loop\n")
    exploreTreeLoop(printNodes)
