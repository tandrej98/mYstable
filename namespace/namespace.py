"""
    The namespace.py module. This module manage virtual spaces and their
    properties.

    Copyright (C) {2021}  {Alica Ondreakova}
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
This module manage virtual spaces and their properties.

Classes
-------
Node 
    bitmask of Node is stored here

NameSpace
    spaces management, addition, removal and cycle detection error

VirtualSpace
    properties of space are stored here


"""

import sys
import graphlib
import treelib
import hashlib
from itertools import chain
from typing import Optional


class Node:
    """
    A class where bitmask of a Node is stored and managed.

    ...

    Attributes
    ----------
    path : str
        name of given Node.
    spaces_mask : int
        bitmask of a given Node

    Methods
    -------
    space_mask_test(space_id):
        returns true if the bit is on.

    spaces_mask_set(space_id):
        activate bit with given id.

    spaces_mask_unset(space_id):
        deactivate bit with given id.
    """

    def __init__(self, path: str) -> None:
        """
        Constructor of Node class, neccesary attributes are here.
        
        Each Node has its own bitmask(space_mask). Each bit represents one
        space, if is bit set to 1 given Node belongs to this space, otherwise
        not.

        Parameters
        ----------
        path : str
            name of given Node.
        """
        self.path = path
        self.spaces_mask = 0

    def spaces_mask_test(self, space_id: int) -> bool:
        """
        Take bitmask of a given Node and make logical AND operation with second
        bitmask where is n-th bit active.

        Parameters
        ----------
        space_id : int
            index of space we want to activate.

        Returns
        -------
        True or False, if a space is activate returns True .
        """
        return (self.spaces_mask & (1 << space_id)) != 0

    def spaces_mask_set(self, space_id: int) -> None:
        """
        Take bitmask of a Node and make logical OR with bitmask where is n-th
        bit activated.

        Parameters
        ----------
        space_id : int
            index of space we want to activate.

        Returns
        -------
        None
        """
        self.spaces_mask = self.spaces_mask | (1 << space_id)

    def spaces_mask_unset(self, space_id: int) -> None:
        """
        Take bitmask of a Node and make logical AND with bitmask where is n-th
        bit activated.

        Parameters
        ----------
        space_id : int
            index of space we want to deactivate.

        Returns
        -------
        None
        """
        self.spaces_mask = self.spaces_mask & ~(1 << space_id)


class NameSpace(object):
    """
    A class which add/substract paths to spaces, create nodes from paths, and
    check for cycles.

    ...

    Attributes
    ----------
    counter : int
        number of created spaces
    name_index_map : dict[str, int]
        maps space names to their indices
    tree : treelib.Tree
        name hierarchy tree from paths
    vs : list[VirtualSpace]
        store each space properties



    Methods
    -------
    space(name, create):
        check if space exists if don't make entry into dict, returns index of
        space.

    space_add(s_name, *paths):
        add paths or spaces to denoted lists that are to be added to space

    space_sub(s_name, *paths):
        add paths or spaces to denoted lists that are to be substracted from
        space

    space_test(s_name, *paths):

    _space_add_real(s_name, *paths):
        activate paths in space

    _space_sub_real(s_name, *paths):
        deactivate paths in space

    _build_topo():
        build a topological order from subspaces

    space_update():
        iterate over spaces in topological order and activate/deactivate their
        paths

    _node_for_path(pth):
        create node representation from path componenets

    _unique_digest(pth):
        check if is hash unique if not regenerate

    _get_digest(input):
        create hash from encoded path
    """

    PATH_SECURE_HASH = False
    PATH_DIGEST_LEN = 8

    # _instance = None

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(NameSpace, cls).__new__(cls)
    #         cls._instance.init()
    #     return cls._instance

    def __init__(self) -> None:
        """Constructor of namespace class, spaces are stored here."""
        self.counter = 0
        self.name_index_map = {}
        self.tree = treelib.Tree()
        self.vs = []

    def space(self, name: str, create: bool = True) -> Optional[int]:
        """
        True - create new entry if missing. False - return None if does not
        exist.

        Parameters
        ----------
        name : str
            name of space
        create : bool
            True we create new entry, False we return index of space
        
        Returns
        -------
        Optional[int] index of given space
        """
        if name not in self.name_index_map:
            if not create:
                return None
            index = self.counter
            self.name_index_map[name] = index
            self.counter += 1
            self.vs.append(VirtualSpace(name, index))
            return index
        return self.name_index_map[name]

    def space_add(self, s_name: str, *paths: str) -> None:
        """
        Add paths or spaces to denoted lists that are to be added to space.

        Parameters
        ----------
        s_name : str
            name of space
        *paths : str
            pahts we want to add to space

        Returns
        -------
        None
        """
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_add.append(pth)
            else:
                self.vs[space_id].nodes_add.append(pth)

    def space_sub(self, s_name: str, *paths: str) -> None:
        """
        Add paths or spaces to denoted lists that are to be substracted from
        space.

        Parameters
        ----------
        s_name : str
            name of space
        *paths : str
            paths that we want to substract from space

        Returns
        -------
        None
        """
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_sub.append(pth)
            else:
                self.vs[space_id].nodes_sub.append(pth)

    def space_test(self, s_name: str, *paths: str) -> bool:
        """
        TODO.

        TODO.

        Parameters
        ----------
        s_name : str
            name of space
        *paths : str
            pahts to be added

        Returns
        -------
        bool
        """
        space_id = self.space(s_name)
        return all(
            self._node_for_path(path).spaces_mask_test(space_id)
            for path in paths)

    def _space_add_real(self, s_name: str, *paths: str) -> None:
        """
        Activate paths in space.

        Parameters
        ----------
        s_name : str
            name of space
        *paths : str
            paths that will be active for space

        Returns
        -------
        None
        """
        space_id = self.space(s_name)
        self.vs[space_id].nodes.update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_set(space_id)

    def _space_sub_real(self, s_name: str, *paths: str) -> None:
        """
        Deactivate paths in space.

        Parameters
        ----------
        s_name : str
            name of space
        *paths : str
            paths that will be unactive for space

        Return
        ------
        None
        """
        space_id = self.space(s_name)
        self.vs[space_id].nodes.difference_update(paths)
        for pth in paths:
            node = self._node_for_path(pth)
            node.spaces_mask_unset(space_id)

    def _build_topo(self) -> list[int]:
        """
        Build topological order from spaces, or raise CycleError.

        Parameters
        ----------
        None

        Return
        ------
        *topo.static.order() : list[int]
            list of integers that represent cycle free ordering

        """
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

    def space_update(self) -> None:
        """
        Iterate over spaces and add them or remove them, then clear the list.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
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

    def _node_for_path(self, pth: str) -> Node:
        """
        Build a tree from path components. Each path component is transformed
        to Node.

        Parameters
        ----------
        pth : str
            path from which is node created
        Return
        ------
        node.data : Node
            returns node data
        """
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

    def _unique_digest(self, pth: str) -> bytes:
        """
        Encode our input and generate hash until its unique.

        Parameters
        ----------
        pth : str
            component of path that is feeded to hasher

        Returns
        -------
        digest : bytes
            return unique 8 byte hash(identified of node)

        """
        digest = pth.encode("utf-8")
        node = None
        while True:
            digest = self._get_digest(digest)
            digest = digest[:self.PATH_DIGEST_LEN]
            node = self.tree.get_node(digest)
            if node is None or node.data.path == pth:
                break
        return digest, node

    def _get_digest(self, input: bytes) -> bytes:
        """
        Create a digest from bytes.

        Parameters
        ----------
        input : bytes
            encoded componenent that is feeded to hasher

        Return
        ------
        hasher.digest() : bytes
            returns one-way, non-cryptographic hash
        """
        hasher = hashlib.md5(usedforsecurity=self.PATH_SECURE_HASH)
        hasher.update(input)
        return hasher.digest()


class VirtualSpace:
    """
    A class which store properties of virtual space.

    ...

    Attributes
    ----------
    name : str
        name of space
    index : int
        index of given space
    nodes : set[Node]
        set of Nodes of virtual space
    nodes_add : list
        represent nodes to be added
    nodes_sub : list
        represent nodes to be removed
    subspaces_add : list
        represent virtual spaces that will be added
    subspaces_sub : list
        represent virtual spaces that will be removed
    """

    def __init__(self, name: str, index: int) -> None:
        """
        Constructor of VirtualSpace, initialize properties of virtual space.

        Parameters
        ----------
        name : str
            name of virtual space
        index : int 
            index of virtual space

        Returns
        -------
        None
        """
        self.name = name
        self.index = index
        self.nodes = set()
        self.nodes_add = []
        self.nodes_sub = []
        self.subspaces_add = []
        self.subspaces_sub = []
