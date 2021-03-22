import treelib
import tree


def show_tree():
    mt = tree.NameSpace()
    mt.space_add(
            'kento', 'etc/gss/bc', 'etc/ssh/id_rsa', '/home/user/elis/images',
            '/home/user/david/documents/','e/sitepackages/tree',
        )
    mt.space_add(
            'funko', 'etc/gss/bc', 'etc/ssh/id_rsa', '/home/user/elis/images',
            '/home/user/david/documents/','e/sitepackages/tree',
        )

    mt.tree.show()
    print(mt.vw.spaces_add)
   
    print(mt.name_index_map['kento'])
    print((mt.vw.nodes[0]))




show_tree()
