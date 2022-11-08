"""
    Tree structure for namespace.py module. Initialize and fill instance of
    tree class. Shows name hierarchy from components.

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
Initialize and fill instance of tree class. Shows name hierarchy from 
components.

"""
import namespace
import treelib.tree


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
    mt = namespace.NameSpace()
    mt.space_add(
        'kento',
        '/etc/gss/bc',
        '/etc/ssh/id_rsa',
        '/home/user/elis/images',
        '/home/user/david/documents/',
        '/e/sitepackages/tree',
        '/etc/.*'
    )
    mt.space_add(
        'kirk',
        '/etc/gss/bc',
        '/etc/gss/ab',
        '/home/.*',
        '/home/user/elis/images'
    )

    mt.space_update()

    print('tree after adding')
    space_contains(mt, 'kento', '/etc/gss/bc')
    space_contains(mt, 'kento', 'etc/ssh/id_rsa')
    space_contains(mt, 'kento', '/home/user/elis/images')
    space_contains(mt, 'kento', '/home/user/david/documents/')
    space_contains(mt, 'kento', '/etc/gss/ab')
    space_contains(mt, 'kirk', '/etc/gss/ab')
    space_contains(mt, 'kirk', '/etc/gss/bc')
    space_contains(mt, 'kirk', '/home/user/elis/images')
    mt.print()

    mt.space_sub('kento', '/home/user/elis/images')
    mt.space_sub('kirk', '/home/user/elis/images')
    mt.space_update()

    print('tree after removing')
    space_contains(mt, 'kento', '/home/user/elis/images')
    space_contains(mt, 'kirk', '/home/user/elis/images')
    mt.print()


def space_contains(name_space: namespace.NameSpace, space: str, path: str):
    """
    Print whether the virtual space in namespace contains the path.

    Parameters
    ----------
    name_space : namespace.NameSpace
            NameSpace to work with
    space : str
            name of virtual space we want to check the path in
    path : str
            path which existence to check in virtual space

    Returns
    -------
    None
    """
    result = name_space.space_test(space, path)
    print(f'space: {space}, path: {path}, result: {result}')


show_tree()
