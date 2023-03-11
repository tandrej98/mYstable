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
import re
from itertools import chain
from typing import Optional
from os.path import normpath, basename, split, join
from collections import defaultdict


def _find_recursive_node(nodes: list) -> treelib.node.Node | None:
    """
    Find recursive node in specified list of nodes.

    Parameters
    ----------
    nodes : list
        list of nodes to be searched for a node with recursive tag

    Returns
    ------
    treelib.node.Node if found, None if not
    """
    return next(filter(lambda c: c.tag == '.*', nodes), None)


class SpaceBitmask:
    """
    A class where bitmask data about active spaces and whether they were
    activated by a rule or not is stored and managed.

    ...

    Attributes
    ----------
    space_mask : int
        bitmask containing active spaces
    by_rule_mask : int
        bitmask that tracks if the space was set by a rule

    Methods
    -------
    is_space_set(space_id):
        Check if requested bit is set.

    mask_set(space_id):
        Activate bit with given id.

    mask_unset(space_id):
        Deactivate bit with given id.

    was_set_by_rule():
        Check if the requested space was set by a rule.
    """
    def __init__(self):
        """
        Constructor of SpaceBitMask class, necessary attributes are initialized
        here.

        Each Node has its own bitmask(space_mask). Each bit represents one
        space, if is bit set to 1 given Node belongs to this space, otherwise
        not.

        Parameters
        ----------
        None
        """
        self.space_mask = 0
        self.by_rule_mask = 0

    def mask_set(self, space_id: int, by_rule: bool = True) -> None:
        """
        Set the space_id-th bit in this bitmask. Use logical OR between this
        bitmask and a bitmask where is space_id-th bit is set.

        Parameters
        ----------
        space_id : int
            index of space we want to activate.
        by_rule : bool
            tracks if space was set by a rule or not

        Returns
        -------
        None
        """
        if by_rule:
            self.by_rule_mask = self.by_rule_mask | (1 << space_id)

        self.space_mask = self.space_mask | (1 << space_id)

    def mask_unset(self, space_id: int, by_rule: bool = True):
        """
        Unset the space_id-th bit in this bitmask. Use logical AND between this
        bitmask and a bitmask where is space_id-th bit is unset.

        Parameters
        ----------
        space_id : int
            index of space we want to deactivate.
        by_rule : bool
            tracks if space was unset by a rule or not

        Returns
        -------
        None
        """
        if by_rule:
            self.by_rule_mask = self.by_rule_mask | (1 << space_id)

        self.space_mask = self.space_mask & ~(1 << space_id)

    def is_space_set(self, space_id: int) -> bool:
        """
        Check the space bitmask if the space is active. Logical AND between
        this bitmask and the supplied one is used.

        Parameters
        ----------
        space_id : int
            index of space we want to test.

        Returns
        -------
        True or False, representing whether the space is set in this mask.
        """
        return (self.space_mask & (1 << space_id)) != 0

    def was_set_by_rule(self, space_id: int) -> bool:
        """
        Check if a space was set by a rule or not. Take by rule bitmask and do
        logical AND operation with second bitmask where only space_id-th bit
        is set.

        Parameters
        ----------
        space_id : int
            index of space we want to check if set by rule.

        Returns
        -------
        True or False, if checked space was set by a rule returns True .
        """
        return (self.by_rule_mask & (1 << space_id)) != 0


def prep_space_info(index: int, mask: SpaceBitmask) -> str:
    """
    Prepare a string with virtual space name and the inherited (I) flag if
    needed.

    Parameters
    ----------
    index : int
        index of space we want to process.
    mask: SpaceBitmask
        mask in which we want to check the presence of the virtual space

    Returns
    -------
    String with virtual space name and needed flags.
    """
    is_inherited = f'{"" if mask.was_set_by_rule(index) else "(I)"}'
    return f'{Node.vs[index].name}{is_inherited}'


class Node:
    """
    A class where bitmask of a Node is stored and managed.

    ...

    Attributes
    ----------
    vs : list
        a class attribute containing a list of all existing virtual spaces
    path : str
        name of given Node.
    positive_mask : SpaceBitmask
        bitmask tracking enabled spaces
    negative_mask : SpaceBitmask
        bitmask tracking disabled spaces
    created_by_rule : bool
        track whether node created by rule or not

    Methods
    -------
    space_mask_test(space_id):
        returns true if the bit is on.

    spaces_mask_set(space_id):
        activate bit with given id.

    spaces_mask_unset(space_id):
        deactivate bit with given id.

    node_info():
        Return string with information needed for printing.
    """

    vs = []

    def __init__(self, path: str, created_by_rule: bool = False) -> None:
        """
        Constructor of Node class, neccesary attributes are here.
        
        Each Node has its own bitmask(space_mask). Each bit represents one
        space, if is bit set to 1 given Node belongs to this space, otherwise
        not.

        Parameters
        ----------
        path : str
            Name of given Node.
        created_by_rule : bool
            Is Node created by rule or not.
        """
        self.path = path
        self.positive_mask = SpaceBitmask()
        self.negative_mask = SpaceBitmask()
        self.created_by_rule = created_by_rule

    def spaces_mask_test(self, space_id: int) -> bool:
        """
        Take bitmask of a given Node and check if the space is set in positive
        bitmask and also not set in negative bitmask.

        Parameters
        ----------
        space_id : int
            index of space we want to activate.

        Returns
        -------
        True or False, if a space is active returns True .
        """
        return self.positive_mask.is_space_set(space_id) and\
            not self.negative_mask.is_space_set(space_id)

    def spaces_mask_set(self, space_id: int, by_rule: bool = True) -> None:
        """
        Activate space by setting space as active in the positive bitmask of
        this Node.

        Parameters
        ----------
        space_id : int
            index of space we want to activate.
        by_rule : bool
            tracks if space was set by a rule or not

        Returns
        -------
        None
        """
        self.positive_mask.mask_set(space_id, by_rule)

    def spaces_mask_unset(self, space_id: int, by_rule: bool = True) -> None:
        """
        Deactivate this space by setting space as active in the negative
        bitmask of this Node.

        Parameters
        ----------
        space_id : int
            index of space we want to deactivate.
        by_rule : bool
            tracks if space was set by a rule or not

        Returns
        -------
        None
        """
        self.negative_mask.mask_set(space_id, by_rule)

    def was_added_by_rule(self, space_id: int) -> bool:
        """
        Check if a space was set by a rule or not. Take bitmask of spaces
        activated by a rule and do logical AND operation with
        second bitmask where only n-th bit active.

        Parameters
        ----------
        space_id : int
            index of space we want to check if set by rule.

        Returns
        -------
        True or False, if a space was added by a rule returns True .
        """

        if self.negative_mask.is_space_set(space_id):
            active_mask = self.negative_mask
        else:
            active_mask = self.positive_mask
        return active_mask.was_set_by_rule(space_id)

    def active_spaces(self) -> list[int]:
        """
        Construct a list of virtual spaces that this node belongs to.

        Parameters
        ----------
        None

        Returns
        ------
        list of space names that this node belongs to.
        """
        virtual_spaces = []
        for space in Node.vs:
            if self.spaces_mask_test(space.index):
                virtual_spaces.append(space.index)
        return virtual_spaces

    @property
    def node_info(self) -> str:
        """
        Create a string containing the tag of this node and other information
        needed for printing. For Namespace root empty string is returned.

        Parameters
        ----------
        None

        Returns
        -------
        String containing information needed for printing the node.
        """
        if self.path == '':
            return ''

        vs = []
        name = basename(normpath(self.path))
        by_rule = f'{"(R)" if self.created_by_rule else ""}'

        for i, v in enumerate(Node.vs):
            if self.positive_mask.is_space_set(i):
                vs.append(prep_space_info(i, self.positive_mask))
            if self.negative_mask.is_space_set(i):
                vs.append('-' + prep_space_info(i, self.negative_mask))

        return f'{name}{by_rule} vs={vs}'


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
    processing_rules : bool
        track whether the namespace is processing rules or inheritance
    interpreter : RuleInterpreter
        interprets custom regex paths



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

    print():
        Print the contents of the namespace.

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
        self.vs = Node.vs
        self.processing_rules = True
        self.interpreter = RuleInterpreter()

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
            if pth[0] == '/' or pth.startswith(RuleInterpreter.recursive_pref):
                new_adds, new_subs = self.interpreter.interpret_add_rule(pth)
                self.vs[space_id].nodes_add.extend(new_adds)
                self.vs[space_id].nodes_sub.extend(new_subs)

            else:
                self.vs[space_id].subspaces_add.append(pth)

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
        # TODO: interpret sub paths
        space_id = self.space(s_name)
        for pth in paths:
            if pth[0] != '/':
                self.vs[space_id].subspaces_sub.append(pth)
            else:
                self.vs[space_id].nodes_sub.append(pth)

    def space_test(self, s_name: str, *paths: str) -> bool:
        """
        Check whether the supplied space contains all the paths.

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

    def print(self):
        """
        Print the contents of the namespace.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        print(f'(I) - Space added by inheritance\n(R) - Node created by rule')
        self.tree.show(data_property='node_info')

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
            node = self._node_for_path(pth, True)
            node.spaces_mask_set(space_id, self.processing_rules)

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
            node = self._node_for_path(pth, True)
            node.spaces_mask_unset(space_id, self.processing_rules)

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
        Update the namespace tree by rules and check for cycles. Then apply
        rule inheritance for regexes and check again.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        self._space_update_internal()
        self.processing_rules = False
        self._process_regex_nodes()
        self._space_update_internal()

    def _recursive_spaces(self, nid: bytes, pth: str, new_nodes: dict) -> list:
        """
        Find all spaces the recursive sibling of node with nid belongs to.

        Parameters
        ----------
        nid : bytes
            node id of target node
        pth : str
            path of target node
        new_nodes : dict
            a dictionary of path -> space_id, of nodes yet to be added to tree

        Returns
        ------
        list of spaces the selected nodes recursive child should belong to
        """
        siblings = self.tree.siblings(nid)
        rec_sibling = _find_recursive_node(siblings)

        if isinstance(rec_sibling, treelib.node.Node):
            rec_spaces = rec_sibling.data.active_spaces()
        else:
            rec_spaces = list()

        rec_sibling_pth = join(split(pth)[0], '.*')
        rec_spaces.extend(new_nodes[rec_sibling_pth])

        return rec_spaces

    def _process_regex_nodes(self) -> None:
        """
        Process inheriting and limiting spaces by regex nodes after tree with
        simple rules created.

        Parameters
        ----------
        None

        Return
        ------
        None
        """
        # TODO: only processing adding nodes, so far
        added_nodes = defaultdict(list)
        for nid in self.tree.expand_tree(
                filter=lambda n: '.*' != n.tag
        ):
            if _find_recursive_node(self.tree.children(nid)) is None:
                path = self.tree.get_node(nid).data.path
                if self.tree.root == nid:
                    self._node_for_path(join(path, '.*'), True)
                else:
                    # As tree is searched from root in depth, the parent node
                    # should already have an initialized recursive node
                    rec_path = join(path, '.*')
                    parent_recursive_spaces = \
                        self._recursive_spaces(nid, path, added_nodes)

                    if not parent_recursive_spaces:
                        self._node_for_path(rec_path, True)
                    for space_id in parent_recursive_spaces:
                        self.vs[space_id].nodes_add.append(rec_path)
                        added_nodes[rec_path].append(space_id)

    def _space_update_internal(self) -> None:
        """
        Internal version of space update. Iterate over spaces and add them or
        remove them, then clear the list.

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

    def _node_for_path(self, pth: str, is_creation: bool = False) -> Node:
        """
        Build a tree from path components. Each path component is transformed
        to Node.

        Parameters
        ----------
        pth : str
            path from which is node created
        is_creation : bool
            tracks if node is expected to be created or only tested
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
        if is_creation and self.processing_rules:
            node.data.created_by_rule = True
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


class RuleInterpreter:
    """
    A class which interprets custom regex rules to basic add and sub rules.

    ...

    Attributes
    ----------
    recursive_pref : str
        a constant holding the recursive configuration keyword
    single_rec_block : str
        a constant holding the single asterisk child suffix
    double_rec_block : str
        a constant holding the double asterisk child suffix
    recursive_regex: str
        a constant holding the recursive regex constant



    Methods
    -------
    interpret_add_rule(path):
        translate custom regex add rules to simple add rules
    _proc_ending(paths):
        translate custom regex add rules at the end of the processed rule
    _proc_middle(path):
        translate custom regex add rules not at the end of the processed rule
    _proc_single_mid_rec_rule(path):
        translate custom * regex that is not at the ned of the processed rule
    _validate_rule(path):
        validate the rule and log the necessary information
    """
    recursive_pref = 'recursive '
    single_rec_block = '*'
    double_rec_block = '**'
    recursive_regex = '.*'
    cust_double_non_end = re.compile(r'\*\*(?!/$)(?!$)')
    cust_single_non_end = re.compile(r'/\*/(?!/$)(?!$)')

    def interpret_add_rule(self, path: str) -> tuple[list[str], list[str]]:
        """
        Translate a custom regex input rule to simple add rules.

        Parameters
        ----------
        path : str
            input rule path to be translated

        Return
        ------
        add_paths : list[str]
            a list of translated simple add rules
        sub_paths : list[str]
            a list of translated simple sub rules
        """
        self._validate_rule(path)
        add_rules = []
        sub_rules = []

        add_processed, sub_processed = self._proc_middle(path)

        add_ending, sub_ending = self._proc_ending([add_processed])
        add_rules.extend(add_ending)
        sub_rules.extend(sub_ending)

        add_ending, sub_ending = self._proc_ending(sub_processed)
        sub_rules.extend(add_ending)
        sub_rules.extend(sub_ending)

        return add_rules, sub_rules

    def _proc_ending(self, paths: list[str]) -> tuple[list[str], list[str]]:
        """
        Translate custom regex ending blocks of the processed rule.

        Parameters
        ----------
        paths : list[str]
            input rule paths to be translated

        Return
        ------
        add_paths : list[str]
            a list of translated simple add rules
        sub_paths : list[str]
            a list of translated simple sub rules
        """
        add_paths = []
        sub_paths = []

        for path in paths:
            is_recursive = False
            is_double_rec_suf = False
            is_single_rec_suf = False

            if path.startswith(self.recursive_pref):
                path = path.removeprefix(self.recursive_pref)
                is_recursive = True

            if path.endswith(self.double_rec_block):
                is_double_rec_suf = True
                path = path.removesuffix(self.double_rec_block)
            elif path.endswith(self.single_rec_block):
                is_single_rec_suf = True
                path = path.removesuffix(self.single_rec_block)

            is_rec_suf = is_single_rec_suf or is_double_rec_suf

            if is_recursive and not is_rec_suf:
                add_paths.append(path)
                add_paths.append(join(path, self.recursive_regex))
            elif is_double_rec_suf or (is_recursive and is_single_rec_suf):
                add_paths.append(join(path, self.recursive_regex))
            elif not is_recursive and is_single_rec_suf:
                first_child_pth = join(path, self.recursive_regex)
                add_paths.append(join(first_child_pth))
                sub_paths.append(join(first_child_pth, self.recursive_regex))
            else:
                add_paths.append(path)

        return add_paths, sub_paths

    def _proc_middle(self, path: str) -> tuple[str, list[str]]:
        """
        Translate custom regex blocks that are not the ending blocks of the
        processed rule.

        Parameters
        ----------
        path : str
            input rule path to be translated

        Return
        ------
        add_paths : list[str]
            a list of translated simple add rules
        sub_paths : list[str]
            a list of translated simple sub rules
        """
        substituted = re.sub(
                self.cust_double_non_end,
                self.recursive_regex,
                path
            )
        processed = self._proc_single_mid_rec_rule(substituted)
        return processed[0], processed[1:]

    def _proc_single_mid_rec_rule(self, path: str) -> list[str]:
        """
        Translate custom single asterix regex blocks that are not the ending
        blocks of the processed rule.

        !CAUTION!: recursion is used, computation time is 2^n because every
        /*/ block creates two rules by itself

        Parameters
        ----------
        path : str
            input rule path to be translated

        Return
        ------
        output : list[str]
            a list of translated simple rules, first is add-rules, others are
            sub-rules
        """
        if not re.search(self.cust_single_non_end, path):
            return [path]

        output = []
        output.extend(
            self._proc_single_mid_rec_rule(
                re.sub(self.cust_single_non_end, '/.*/', path, 1)
            )
        )
        output.extend(
            self._proc_single_mid_rec_rule(
                re.sub(self.cust_single_non_end, '/.*/.*/', path, 1)
            )
        )
        return output

    def _validate_rule(self, path: str) -> None:
        """
        Check that the input rule is valid.

        Parameters
        ----------
        path : str
            input rule path to be validated

        Return
        ------
        None
        """
        path_parts = path.split(self.recursive_pref)
        if len(path_parts) > 1 and path_parts[1][0] != '/':
            raise ValueError("A subspace cannot use recursive keyword")


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
