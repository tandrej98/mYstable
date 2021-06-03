# bp1
Module for mYstable Authorization server, not yet integrated based on abstraction of Constable's Authorization server.

__*Prerequisites*__: Python3.6 >=

__*Important*__: From version of Python3.9 >= is graphlib built-in, otherwise installation is needed.

__*Modules*__: treelib (pip install treelib), graphlib (pip install graphlib-backport)

__*Name*__: test_tree.py 
__*Function*__: Testing functionality of tree.py. Unittest framework is used. Addition and removal to spaces is tested with adition to cycle error.

__*Name*__: tree.py  
__*Function*__: Main logic is here, classes: Namespace(addition and substraction of paths/spaces), VirtualSpace(holds info about each space and its properties), 
Node(sets node on/off)

__*Name*__: tree_structure.py 
__*Function*__: Shows tree created from paths.

__*Testing*__: To run unittests <em> python test_tree.py </em> , to show tree structure <em>python tree_strcture.py </em>
