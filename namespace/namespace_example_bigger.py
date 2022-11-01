"""
    Example of a bigger tree structure for namespace.py module. Initialize and
    fill an instance of tree class. Shows name hierarchy and respective virtual
    spaces of components.

    Copyright (C) {2022}  {Andrej Toth}

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import namespace


def show_tree() -> None:
    """
    Fill instance of tree by some data and print resulting tree.

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    ns = namespace.NameSpace()
    ns.space_add('cely_fs', '/', '/.*')

    # TODO: what is this in old config? 'space procesy recursive 'proc';'
    # TODO: 'domain' and 'proc' are on multiple places, where do they fit in?

    ns.space_add('devices', '/dev', '/dev/.*')

    ns.space_add(
        'tty',
        # TODO: uncomment when wider regex support implemented
        # '/dev/[tp]ty.*',
        '/dev/pts',
        '/dev/ptmx',
        '/dev/console',
        # '/dev/vcs.*'
    )

    ns.space_add(
        'userdev',
        '/dev/null',
        '/dev/zero',
        '/dev/random',
        '/dev/urandom'
    )

    ns.space_add(
        'etc',
        '/etc',
        '/etc/.*',
        '/usr/etc',
        '/usr/etc/.*',
        '/usr/local/etc',
        '/usr/local/etc/.*',
        '/proc',
        '/proc/.*',
        '/var/spool/atjobs',
        '/var/spool/atjobs/.*',
        '/var/spool/atspool',
        '/var/spool/atspool/.*',
        '/var/spool/cron',
        '/var/spool/cron/.*',
        '/root',
        '/root/.*'
    )

    # TODO: handle dots in paths
    ns.space_sub(
        'etc',
        '/proc/sys/kernel/modprobe',
        '/etc/fstab',
        '/etc/exports',
        '/etc/inittab',
        '/etc/inetd\\.conf',
        '/etc/lilo\\.conf',
        '/etc/medusa\\.conf',
        '/etc/rbac\\.conf',
        '/etc/modules\\.conf',
        '/etc/ld\\.so\\.cache',
        '/etc/ld\\.so\\.conf',
        '/etc/rc\\.d',
        '/etc/rc\\.d/.*'

    )

    ns.space_add(
        'bin',
        '/bin',
        '/bin/.*',
        '/sbin',
        '/sbin/.*',
        '/lib',
        '/lib/.*',
        '/shlib',
        '/shlib/.*',
        '/boot',
        '/boot/.*',
        '/usr',
        '/usr/.*',
        '/opt',
        '/opt/.*',
        '/home/ftp/bin',
        '/home/ftp/bin/.*',
        '/home/ftp/lib',
        '/home/ftp/lib/.*',
        '/home/ftp/usr',
        '/home/ftp/usr/.*',
        '/',
        '/dev',
        '/var',
        '/etc',
        '/etc/fstab',
        '/etc/exports',
        '/var/lib/nfs',
        '/var/lib/nfs/.*',
        '/etc/inittab',
        '/etc/inetd\\.conf',
        '/etc/lilo\\.conf',
        '/etc/modules\\.conf',
        '/etc/ld\\.so\\.cache',
        '/etc/ld\\.so\\.conf',
        '/etc/rc\\.d',
        '/etc/rc\\.d/.*',
        '/var/X11R6/',
        '/var/X11R6/.*',
        '/proc/sys/kernel/modprobe'
    )

    ns.space_sub(
        'bin',
        '/usr/etc',
        '/usr/etc/.*',
        '/usr/local/etc',
        '/usr/local/etc/.*',
        '/usr/src',
        '/usr/src/.*',
        '/usr/local/src',
        '/usr/local/src/.*',
        '/sbin/constable'
    )

    ns.space_add(
        'medusa',
        '/medusa',
        '/medusa/.*',
        '/etc/medusa\\.conf',
        '/etc/rbac\\.conf',
        '/sbin/constable'
    )

    ns.space_add(
        'var',
        '/var',
        '/var/.*',
        '/var/X11R6',
        '/var/X11R6/.*',
        '/var/spool/mail',
        '/var/spool/mail/.*',
        '/var/spool/atjobs',
        '/var/spool/atjobs/.*',
        '/var/spool/atspool',
        '/var/spool/atspool/.*',
        '/var/spool/cron',
        '/var/spool/cron/.*',
        '/var/lib/nfs',
        '/var/lib/nfs/.*'
    )

    ns.space_add('home', '/home', '/home/.*')

    ns.space_sub('home', '/home/marek/Marek', '/home/marek/Marek/.*')

    ns.space_add(
        'mailbox',
        '/var/spool/mail',
        '/var/spool/mail/.*',
        # TODO: when support for .* added check if works correctly
        '/home/.*/mail',
        '/home/.*/Mail',
        '/home/.*/UNSORTED_MAIL'
    )

    ns.space_add(
        'home_public',
        '/home/.*',
        '/home/.*/.forward',
        '/home/.*/.mailsortrc',
        '/home/.*/.procmailrc',
        '/home/.*/.plan',
        '/home/.*/.project',
        '/home/.*/.tellrc',
        '/home/.*/.screenrc',
        '/home/.*/.terminfo',
        '/home/.*/bin',
        '/home/.*/Bin'
    )

    ns.space_add(
        'web',
        '/services/web-data',
        '/services/web-data/.*',
        '/home/.*/web-data',
        '/home/.*/web-data/.*'
    )

    ns.space_add(
        'ftp',
        '/home/ftp',
        '/home/ftp/.*',
        '/home/.*/incoming',
        '/home/.*/incoming/.*',
        '/home/.*/Incoming',
        '/home/.*/Incoming/.*',
    )

    ns.space_sub(
        'ftp',
        '/home/ftp/bin',
        '/home/ftp/bin/.*',
        '/home/ftp/lib'
        '/home/ftp/lib/.*'
        '/home/ftp/usr',
        '/home/ftp/usr/.*'
    )

    ns.space_add(
        'temp',
        '/temp',
        '/temp/.*',
        '/var/tmp',
        '/var/tmp/.*',
        '/tmp',
        '/var/man',
        '/var/man/.*'
    )

    ns.space_add(
        'data',
        '/services',
        '/services/.*',
        '/cdrom',
        '/cdrom/.*',
        '/mnt',
        '/mnt/.*',
    )

    ns.space_add('skove', '/bin/ping')

    ns.space_add(
        'init',
        'domain/init',
        'proc/',
        'domain/'
    )
    
    ns.space_add(
        'daemon',
        'domain/daemon',
        '/usr/sbin/inetd',
        '/usr/sbin/crond',
        '/usr/sbin/atd',
        '/usr/sbin/apmd'
    )

    ns.space_add('login', 'domain/login', '/bin/login')

    ns.space_add('user', 'domain/user')

    ns.space_add('named', 'domain/named', '/usr/sbin/named')

    ns.space_add('named_data', '/var/named', '/var/named/.*')

    ns.space_add('services', 'web', 'mailbox', 'ftp')

    ns.space_update()
    ns.print()


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
