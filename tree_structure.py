import treelib
import tree
from graphlib import *


def show_tree():
    mt = tree.NameSpace()
    mt.space_add(
        'kento',
        '/etc/gss/bc',
        'etc/ssh/id_rsa',
        '/home/user/elis/images',
        '/home/user/david/documents/',
        '/e/sitepackages/tree',
    )

    mt.space_test('kento', '/etc/gss/bc')
    mt.tree.show()


show_tree()
