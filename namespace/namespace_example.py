"""
    Tree structure for namespace.py module. Initialize and fill instance of tree class. Shows name hierarchy from components.
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
Initialize and fill instance of tree class. Shows name hierarchy from components.

"""
import namespace


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
    )

    mt.space_test('kento', '/etc/gss/bc')
    mt.space_test('kento', 'etc/ssh/id_rsa')
    mt.space_test('kento', '/home/user/elis/images')
    mt.space_test('kento', '/home/user/david/documents/')
    mt.tree.show()


show_tree()
