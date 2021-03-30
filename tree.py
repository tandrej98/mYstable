import sys
import graphlib
import treelib
'''
https://docs.python.org/3/library/graphlib.html?fbclid=IwAR3D0pteYdWhrzimpEqPXOAK_T4rcSkwWP1Z3bksuaxSLpT39_9PyDjJxVg
'''


class NameSpace(object):
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
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_add.append(pth)
            else:
                self.vs[space_id].nodes_add.append(pth)

    def space_sub(self, s_name, *paths):
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
        space_id = self.space(s_name)
        self.vs[space_id].nodes.update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_set(space_id)

    def _space_sub_real(self, s_name, *paths):
        space_id = self.space(s_name)
        self.vs[space_id].nodes.difference_update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_reset(space_id)

    def _build_topo(self, predecessor_proj):
        topo = graphlib.TopologicalSorter()
        for space in self.vs:
            predecessors = []
            for subspace_name in predecessor_proj(space):
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
        try:
            add_topo_order = self._build_topo(
                lambda space: space.subspaces_add)
            sub_topo_order = self._build_topo(
                lambda space: space.subspaces_sub)
        except graphlib.CycleError:
            print("Cycle detected", file=sys.stderr)
            return

        for space_id in add_topo_order:
            space = self.vs[space_id]
            self._space_add_real(space.name, *space.nodes_add)
            for subspace_name in space.subspaces_add:
                subspace_id = self.space(subspace_name, create=False)
                if subspace_id is not None:
                    self._space_add_real(space.name,
                                         *self.vs[subspace_id].nodes)
            space.subspaces_add.clear()
            space.nodes_add.clear()

        for space_id in sub_topo_order:
            space = self.vs[space_id]
            self._space_sub_real(space.name, *space.nodes_sub)
            for subspace_name in space.subspaces_sub:
                subspace_id = self.space(subspace_name, create=False)
                if subspace_id is not None:
                    self._space_sub_real(space.name,
                                         *self.vs[subspace_id].nodes)
            space.subspaces_sub.clear()
            space.nodes_sub.clear()

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
                    node = self.tree.create_node(comp,
                                                 child_pth,
                                                 data=Node(),
                                                 parent=parent_pth)
                parent_pth = child_pth
        return node.data

    def static_order(self):
        self.prepare()
        while self.is_active():
            node_group = self.get_ready()
            yield from node_group
            self.done(*node_group)


class Node:
    def __init__(self):
        self.spaces_mask = 0

    def spaces_mask_test(self, space_id):
        return (self.spaces_mask & (1 << space_id)) != 0

    def spaces_mask_set(self, space_id):
        self.spaces_mask = self.spaces_mask | (1 << space_id)

    def spaces_mask_reset(self, space_id):
        self.spaces_mask = self.spaces_mask & ~(1 << space_id)


class VirtualSpace:
    def __init__(self, name, index):
        self.name = name
        self.index = index
        self.nodes = set()
        self.nodes_add = []
        self.nodes_sub = []
        self.subspaces_add = []
        self.subspaces_sub = []