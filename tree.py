import sys
 
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
        self.tree = treelib.Tree()
        self.vw = []
 
    def space(self, name, create=True): 
        ''' Initialize new VS if doesn't exist, increment counter '''
        if name not in self.name_index_map:
            if not create:
                return None
            index = self.counter
            self.name_index_map[name] = index
            self.counter += 1
            self.vw.append(VirtualWorld(name, index))
            return index
        return self.name_index_map[name]
 

    def space_add(self, s_name, *paths): 
        space_id = self.space(s_name)
        self.vw[space_id].nodes.update(paths)
        for pth in paths:
            if pth[0] == '/':
                node = self._node_for_path(pth)
                node.worlds_mask_set(space_id)
            else:
                self.vw[space_id].spaces_add.append(pth)
                continue
 
    def space_remove(self, s_name, *paths): 
        space_id = self.space(s_name)
        self.vw[space_id].nodes.difference_update(paths)
        for pth in paths:
            if pth[0] == '/':
                node = self._node_for_path(pth)
                node.worlds_mask_reset(space_id)
            else:
                self.vw[space_id].spaces_sub.append(pth)
                continue
 
    def space_test(self, s_name, *paths):
        space_id = self.space(s_name)
        return all(
            self._node_for_path(path).worlds_mask_test(space_id) for path in paths
        )
       
    def space_update(self):
        for space in self.vw:
            for other_space_n in space.spaces_add:
                other_space_id = self.space(other_space_n, create=False)
                if other_space_id is None:
                    print(f"Virtual world {other_space_n} doesn't exist", file=sys.stderr)
                    continue
                else:
                    self.space_add(space.name, *self.vw[other_space_n].nodes)
            space.spaces_add.clear()
 
            for other_space_n in space.spaces_sub:
                other_space_id = self.space(other_space_n, create=False)
                if other_space_id is None:
                    print(f"Virtual world {other_space_n} doesn't exist", file=sys.stderr)
                    continue
                else:
                    self.space_remove(space.name, *self.vw[other_space_n].nodes)
            space.spaces_sub.clear()
 
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
 
 
class VirtualWorld:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.nodes = set()
        self.spaces_add = []
        self.spaces_sub = []