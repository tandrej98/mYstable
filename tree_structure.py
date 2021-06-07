"""
Initialize and fill instance of tree class. Shows name hierarchy from components.

"""
import treelib
import tree
from graphlib import *


def show_tree() -> None:
    """
    Fill instance of tree by some data.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    mt = tree.NameSpace()
    mt.space_add(
        'kento',
        '/etc/gss/bc',
        '/etc/ssh/id_rsa',
        '/home/user/elis/images',
        '/home/user/david/documents/',
        '/e/sitepackages/tree',
    )

    mt.space_test('kento', '/etc/gss/bc')
    mt.space_test('kento', 'etc/ssh/id_rsa')
    mt.space_test('kento', '/home/user/elis/images')
    mt.space_test('kento', '/home/user/david/documents/')
    mt.tree.show()


show_tree()

