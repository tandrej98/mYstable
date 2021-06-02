import sys
import graphlib
import treelib
import hashlib
from itertools import chain
 

class NameSpace(object):
    PATH_HASH_ALG = 'md5'
    PATH_SECURE_HASH = False
    PATH_DIGEST_LEN = 8
 
    ''' '''
    # _instance = None
 
    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(NameSpace, cls).__new__(cls)
    #         cls._instance.init()
    #     return cls._instance
 
    def __init__(self):
        self.counter = 0
        self.name_index_map = {}
        self.tree = treelib.Tree()
        self.vs = []
 
    def space(self, name, create=True):
        ''' Initialize new VS if doesn't exist, increment counter '''
        if name not in self.name_index_map:
            if not create:
                return None
            index = self.counter
            self.name_index_map[name] = index
            self.counter += 1
            self.vs.append(VirtualSpace(name, index))
            return index
        return self.name_index_map[name]
 
    def space_add(self, s_name, *paths):
        ''' Add paths or spaces to denoted lists that are to be added from vs '''
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_add.append(pth)
            else:
                self.vs[space_id].nodes_add.append(pth)
 
    def space_sub(self, s_name, *paths):
        ''' Add paths or spaces to denoted lists that are to be removed from vs '''
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_sub.append(pth)
            else:
                self.vs[space_id].nodes_sub.append(pth)
 
    def space_test(self, s_name, *paths):
        space_id = self.space(s_name)
        return all(
            self._node_for_path(path).spaces_mask_test(space_id)
            for path in paths)
 
    def _space_add_real(self, s_name, *paths):
        ''' Set mask on for paths in space '''
        space_id = self.space(s_name)
        self.vs[space_id].nodes.update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_set(space_id)
 
    def _space_sub_real(self, s_name, *paths):
        ''' Unset mask on for paths in space '''
        space_id = self.space(s_name)
        self.vs[space_id].nodes.difference_update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_unset(space_id)
 
    def _build_topo(self):
        ''' Build topological order from spaces, or raise CycleError'''
        topo = graphlib.TopologicalSorter()
        for space in self.vs:
            predecessors = []
            for subspace_name in chain(space.subspaces_add, space.subspaces_sub):
                subspace_id = self.space(subspace_name, create=False)
                if subspace_id is None:
                    print(f"Virtual world {subspace_name} doesn't exist",
                          file=sys.stderr)
                    continue
                else:
                    predecessors.append(subspace_id)
            topo.add(space.index, *predecessors)
 
        return [*topo.static_order()]
 
    def space_update(self):
        ''' Iterate over spaces and add them or remove them, then clear the list '''
        try:
            topo_order = self._build_topo()
        except graphlib.CycleError:
            print("Cycle detected", file=sys.stderr)
            return
 
        for space_id in topo_order:
            space = self.vs[space_id]
            self._space_add_real(space.name, *space.nodes_add)
            for subspace_name in space.subspaces_add:
                subspace_id = self.space(subspace_name, create=False)
                if subspace_id is not None:
                    self._space_add_real(space.name,
                                         *self.vs[subspace_id].nodes)
            space.subspaces_add.clear()
            space.nodes_add.clear()
 
            self._space_sub_real(space.name, *space.nodes_sub)
            for subspace_name in space.subspaces_sub:
                subspace_id = self.space(subspace_name, create=False)
                if subspace_id is not None:
                    self._space_sub_real(space.name,
                                         *self.vs[subspace_id].nodes)
            space.subspaces_sub.clear()
            space.nodes_sub.clear()
 
    def _node_for_path(self, pth):
        ''' Build a tree from paths '''
        pth_digest, node = self._unique_digest(pth)
 
        if node is None:
            components = pth.split('/')
            parent_pth = None
            parent_pth_digest = None
            for comp in components:
                if parent_pth is None:
                    child_pth = ""
                else:
                    child_pth = parent_pth + "/" + comp
                child_pth_digest, node = self._unique_digest(child_pth)
                if node is None:
                    node = self.tree.create_node(tag=comp,
                                                 identifier=child_pth_digest,
                                                 parent=parent_pth_digest,
                                                 data=Node(child_pth))
                parent_pth = child_pth
                parent_pth_digest = child_pth_digest
        return node.data
 
    def _unique_digest(self, pth):
        ''' Encode our input and generate hash until its unique '''
        digest = pth.encode("utf-8")
        node = None
        while True:
            digest = self._get_digest(digest)
            digest = digest[:self.PATH_DIGEST_LEN]
            node = self.tree.get_node(digest)
            if node is None or node.data.path == pth:
                break
        return digest, node
 
    def _get_digest(self, input):
        ''' Create a digest of the input byte sequence '''
        hasher = hashlib.new(self.PATH_HASH_ALG, usedforsecurity=self.PATH_SECURE_HASH)
        hasher.update(input)
        return hasher.digest()

 
class Node:
    def __init__(self, path):
        self.path = path
        self.spaces_mask = 0
 
    def spaces_mask_test(self, space_id):
        return (self.spaces_mask & (1 << space_id)) != 0
 
    def spaces_mask_set(self, space_id):
        ''' We turn the bit on '''
        self.spaces_mask = self.spaces_mask | (1 << space_id)
 
    def spaces_mask_unset(self, space_id):
        ''' We turn the bit off '''
        self.spaces_mask = self.spaces_mask & ~(1 << space_id)
 
 
class VirtualSpace:
    ''' Each space has it's unique prop '''
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.nodes = set()
        self.nodes_add = []
        self.nodes_sub = []
        self.subspaces_add = []
        self.subspaces_sub = []