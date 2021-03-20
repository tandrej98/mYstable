import treelib


class NameSpace(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NameSpace, cls).__new__(cls)
            cls._instance.init()
        return cls._instance

    def init(self):
        self.counter = 0
        self.name_index_map = {}
        self.nodes = []
        self.tree = treelib.Tree()

    def space(self, name): 
        if name not in self.name_index_map:
            index = self.counter
            self.name_index_map[name] = index
            self.counter += 1
            self.nodes.append(set())
            return index
        return self.name_index_map[name]

    def space_add(self, s_name, *paths): #TODO add also space  and all its paths to mask set, /
        space_id = self.space(s_name)
        self.nodes[space_id].update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.worlds_mask_set(space_id)

    def space_remove(self, s_name, *paths): #TODO add also space() and all its paths to mask set, /
        space_id = self.space(s_name)
        self.nodes[space_id].difference_update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.worlds_mask_reset(space_id)

    def space_test(self, s_name, *paths):
        space_id = self.space(s_name)
        return all(
            self._node_for_path(path).worlds_mask_test(space_id) for path in paths
        )
       
    def _node_for_path(self, pth):
        node = self.tree.get_node(pth)
        if node is None:
            components = pth.split('/')
            parent_pth = None
            for comp in components:
                if parent_pth is None:
                    child_pth = ""
                else:
                    child_pth = parent_pth + "/" + comp
                node = self.tree.get_node(child_pth)
                if node is None:
                    node = self.tree.create_node(comp, child_pth, data=Node(), parent=parent_pth)
                parent_pth = child_pth
        return node.data


class Node:
    def __init__(self):
        self.worlds_mask = 0
    
    def worlds_mask_test(self, space_id):
        return (self.worlds_mask & (1 << space_id)) != 0
    
    def worlds_mask_set(self, space_id):
        self.worlds_mask = self.worlds_mask | (1 << space_id)
    
    def worlds_mask_reset(self, space_id):
        self.worlds_mask = self.worlds_mask & ~(1 << space_id)


