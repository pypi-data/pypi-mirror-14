#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             node.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/03/2015
#
# pylint:           disable=line-too-long

"""
ext_pylib.files.node
~~~~~~~~~~~~~~~~~~~~

An abstract class that describes a node to be extended by a directory and file
class respectively.
"""

from __future__ import absolute_import, print_function, unicode_literals

import grp
import os
import pwd

from ..user import get_current_username, get_current_groupname


class Node(object):
    """An abstract class representing a node object.

    This class is intended primarily as a wrapper for directory and file
    management and is designed to be extended by file and directory classes.

    Node is initialized with a dict of attributes. Attributes that aren't given
    are just initialized as None. If a path isn't given, the node is set to
    path = None. This effectively makes the Node a "Stub", in which methods do
    nothing but return True (except exists()) enabling a graceful fail.

    :param atts['path']: The path (string) of the node.
    :param atts['perms']: The permissions (int or octal) of the node.
    :param atts['owner']: The owner (string) of the node.
    :param atts['group']: The group (string) of the node.

    * Note: This class is intended to be subclassed.

    Usage::

        >>> from ext_pylib.files.node import Node

        >>> node = Node({'path' : '/the/path/', 'perms' : 0o600, 'owner' : 'root', 'group' : 'root'})
        >>> node.path
        '/the/path/'
    """

    def __init__(self, atts=None):
        """Initializes a new Node instance."""
        atts = atts or {}
        if 'path' not in atts:
            self.path = None # !! Make sure path is at least initialized
        for attribute in atts:
            setattr(self, attribute, atts[attribute])

    def __str__(self):
        """Returns a string with the path."""
        if not self.path:
            return '<files.Node:stub>'
        return self.path

    def __repr__(self):
        """Returns a python string that evaluates to the object instance."""
        return "{0}({1})".format(self.__class__.__name__, self.get_atts(string=True))

    def __add__(self, other):
        """Allows string concatenation with the path."""
        return str(self) + other

    def __radd__(self, other):
        """Allows string concatenation with the path."""
        return other + str(self)

    def get_atts(self, string=False):
        """Returns a python string of attributes (as a dict) used to create this object."""
        if not string:
            return {'path' : self.path, 'perms' : getattr(self, '_perms', None), 'owner' : self.owner, 'group' : self.group}
        # Note that any atts added later must be added here for this to work.
        atts = "{'path' : "
        if self.path:
            atts += "'" + self.path + "', "
        else:
            atts += 'None, '

        atts += "'perms' : "
        if self.perms:
            atts += self.perms_as_string() + ", "
        else:
            atts += 'None, '

        atts += "'owner' : "
        if self.owner:
            atts += "'" + self.owner + "', "
        else:
            atts += 'None, '

        atts += "'group' : "
        if self.group:
            atts += "'" + self.group + "'}"
        else:
            atts += 'None}'

        return atts

    @staticmethod
    def create(*args, **kwargs):
        """A stub to be implemented by child class."""
        raise NotImplementedError('[ERROR] Cannot call method on file.Node. It is an abstract class.')

    @staticmethod
    def remove(*args, **kwargs):
        """A stub to be implemented by child class."""
        raise NotImplementedError('[ERROR] Cannot call method on file.Node. It is an abstract class.')

    def chmod(self, perms=None):
        """Sets the permissions on the file/directory."""
        if not self.path:
            return True
        if not self.exists():
            raise IOError(self.path + ' does not exist. Cannot set owner and permissions. [!]')
        if not perms:
            perms = self.perms
        if not perms:
            return True
        print('Setting permissions on ' + self.path + ' to "' + \
              self.perms_as_string(perms)  + '"...', end=' ')
        try:
            os.chmod(self.path, perms) # Be sure to use leading '0' as chmod takes an octal
            print('[OK]')
            return True
        except Exception as error:  # pylint: disable=broad-except
            print('[FAILED]')
            print(error)
            return False

    def chown(self, owner=None, group=None):
        """Sets the owner and group of the directory."""
        if not self.path:
            return True
        if not self.exists():
            raise IOError(self.path + ' does not exist. Cannot set owner and permissions. [!]')
        if not owner:
            owner = self.owner
            if not owner:
                owner = get_current_username()
        if not group:
            group = self.group
            if not group:
                group = 'nogroup' if owner == 'nobody' else get_current_groupname()
        print('Setting owner on ' + self.path + ' to "' + owner  + ':' + group + '"...', end=' ')
        try:
            uid = pwd.getpwnam(owner).pw_uid
            gid = grp.getgrnam(group).gr_gid
            os.chown(self.path, uid, gid)
            print('[OK]')
            return True
        except Exception as error:  # pylint: disable=broad-except
            print('[FAILED]')
            print(error)
            return False

    def exists(self):
        """Returns true if this directory exists on disk."""
        if not self.path:
            return False
        if os.path.exists(self.path):
            return True
        return False

    def verify(self, repair=False):
        """Verifies the existence, permissions, ownership, and group of the file/directory."""
        if not self.path:
            return True
        print('')
        print('Checking "' + self.path + '"...', end=' ')
        if not self.exists():
            print('[WARN]')
            print('[!] ' + self.path + ' doesn\'t exist')
            if not repair:
                return False
            self.create()
            return self.verify(repair)
        print('[OK]')

        # Assume the checks pass
        perms_check = owner_check = group_check = True

        if self.perms:
            print('--> Checking permissions for ' + self.path,)
            perms_check = self.perms == self.actual_perms
            print(' (should be: ' + self.perms_as_string() + ', actual: ' + \
                self.perms_as_string(self.actual_perms) + ')', end=' ')
            print('[OK]' if perms_check else '[WARN]')
            if not perms_check and repair:
                perms_check = self.chmod()
                return self.verify(repair)

        if self.owner:
            print('--> Checking owner for ' + self.path,)
            owner_check = self.owner == self.actual_owner
            print(' (should be: ' + self.owner + ', actual: ' +
                  self.actual_owner + ')', end=' ')
            print('[OK]' if owner_check else '[WARN]')

        if self.group:
            print('--> Checking group for ' + self.path,)
            group_check = self.group == self.actual_group
            print(' (should be: ' + self.group + ', actual: ' + self.actual_group + ')', end=' ')
            print('[OK]' if group_check else '[WARN]')
            if not (group_check or owner_check) and repair:
                group_check = owner_check = self.chown()
                return self.verify(repair)

        result = perms_check and owner_check and group_check

        if not result:
            print('[ERROR] Verification for "' + self.path + '" failed.')

        return result

    def repair(self):
        """Runs verify() with the repair flag set."""
        return self.verify(True)

    @property
    def path(self):
        """Returns the path, if it exists."""
        return getattr(self, '_path', None)

    @path.setter
    def path(self, path):
        """Validates, then sets the path."""
        # pylint: disable=attribute-defined-outside-init
        # Check for None
        if path is None:
            print('[Notice] file.Node was initialized with an empty path.  Continuing as a stub.')
            self._path = None
            return
        # Check for empty string
        if path == '':
            raise ValueError('"path" cannot be set to an empty string in an file.Node class.')
        # Check for valid characters
        for char in path:
            if char not in '-_.() abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/':
                raise ValueError('"' + path + '" is not allowed as an file.Node.')
        # Clean path of extra slashes
        while "//" in path:
            path = path.replace('//', '/')
        self._path = path

    @property
    def name(self):
        """Returns just the name (portion of the path) as a string."""
        path = self.path
        if not path:
            return None
        if path.endswith('/'):  # removes any trailing '/'
            path = path[:-1]
        return path.rsplit('/')[-1]  # last element after splitting based on '/'

    @property
    def parent_node(self):
        """Returns the parent node as a Node object (usually the parent directory)."""
        if not self.path:
            return None
        if self.path == '/':  # '/' has no parent
            return None

        path = self.path
        if not path.endswith('/'):  # makes the spliting easier to have '/' at the end
            path = path + '/'

        if path.endswith('/../'):  # just keep adding /../.. etc... to get parent of relative path.
            parent_path = path + '..'
        elif path.count('/') == 1 and path.endswith('/'):
            # parent of relative path (has only one '/' and ends with it) is <path>/..
            parent_path = path + '..'
        else:
            parent_path = path.rsplit('/', 2)[0] + '/'

        return Node({'path' : parent_path})

    @property
    def actual_perms(self):
        """Returns the perms as it is on disk."""
        if not self.path:
            return None
        return os.stat(self.path).st_mode & 511

    @property
    def perms(self):
        """Returns the perms (oct/int)."""
        return getattr(self, '_perms', None)

    @perms.setter
    def perms(self, perms):
        """Sets the perms (oct/int)."""
        # pylint: disable=attribute-defined-outside-init
        if not perms:
            self._perms = None
            return
        try:
            perms = int(perms)
        except ValueError as error:
            print(error)
            print('[ERROR] ' + perms + ' must be set to an int.')
            raise
        if not 0 <= perms <= 511:
            raise ValueError('"perms" cannot be set to ' + self.perms_as_string(perms) + '.')
        self._perms = perms

    def perms_as_string(self, perms=None):
        """Returns the perms as a string."""
        if not perms:
            if not self.perms:
                return 'None'
            return format(self.perms, '#o')
        return format(perms, '#o')

    @property
    def actual_owner(self):
        """Returns the owner (string) as it is on disk."""
        if not self.path:
            return None
        return pwd.getpwuid(os.stat(self.path).st_uid).pw_name

    @property
    def owner(self):
        """Returns the owner (string)."""
        return getattr(self, '_owner', None)

    @owner.setter
    def owner(self, owner):
        """Sets the owner (string)."""
        # pylint: disable=attribute-defined-outside-init
        if owner is None:
            owner = get_current_username()
        else:
            try:
                # Make sure this is a valid user
                uid = pwd.getpwnam(owner)  # pylint: disable=unused-variable
            except KeyError:
                print('[ERROR] ' + owner + ' is not a valid user.')
                raise
        self._owner = owner

    @property
    def actual_group(self):
        """Returns the group (string) as it is on disk."""
        if not self.path:
            return None
        return grp.getgrgid(os.stat(self.path).st_gid).gr_name

    @property
    def group(self):
        """Returns the group (string)."""
        return getattr(self, '_group', None)

    @group.setter
    def group(self, group):
        """Sets the group (string)."""
        # pylint: disable=attribute-defined-outside-init
        # Check for empty string
        if group is None:
            group = get_current_groupname()
        else:
            try:
                # Make sure this is a valid group
                gid = grp.getgrnam(group) # pylint: disable=unused-variable
            except KeyError:
                print('[ERROR] ' + group + ' is not a valid group.')
                raise
        self._group = group
