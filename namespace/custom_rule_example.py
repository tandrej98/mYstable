"""
    Tree structure for namespace.py module. Initialize and fill instance of
    tree class. Shows name hierarchy from components.

    Copyright (C) {2023}  {Andrej Toth}

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
Demonstrate the effects of each of the possible custom rule. 
"""

import namespace

ns1 = namespace.NameSpace()

paths = ['/etc/xyz',
         'recursive /etc/xyz',
         '/etc/xyz/**',
         'recursive /etc/xyz/**',
         'recursive /etc/xyz/*',
         '/etc/xyz/*',
         '/etc/abc/**/xyz',
         '/etc/abc/*/xyz']


def main():
    """
    Create a separate namespace for add and sub operations for each custom
    rule and print the resulting namespace tree.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    print("ADD RULES")
    for i, v in enumerate(paths):
        print(f'Rule: {v}')
        ns = namespace.NameSpace()
        ns.space_add('x', v)
        ns.space_update()
        ns.print()

    print("SUB RULES")
    for i, v in enumerate(paths):
        print(f'Rule: {v}')
        ns = namespace.NameSpace()
        ns.space_sub('x', v)
        ns.space_update()
        ns.print()


if __name__ == '__main__':
    main()
