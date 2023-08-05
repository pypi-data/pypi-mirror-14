#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             file.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       11/04/2015
#
# pylint:           disable=no-member,line-too-long

"""
ext_pylib.files.file
~~~~~~~~~~~~~~~~~~~~

A class to manage and create files. Also includes three mixin classes Parsable,
Section, and Template.
"""

from __future__ import absolute_import, print_function, unicode_literals

import os
import re

from .dir import Dir
from .node import Node
from ..input import prompt
from ..meta import setdynattr


class File(Node):
    """An class to manage a file's permissions, ownership, and path. Extends Node.
    See Node class for atts to pass in at init.

    The Section mixin adds methods useful for processing template section
    files. A section file is a template of a configuration file that only
    represents a particular section of that file. It begins and ends with a
    delineator (for example: ## START:SECTION_NAME ## and ## END:SECTION_NAME
    ##). A use case would be how WordPress delineates a particular section of
    the htaccess file in its root directory with a start line and an end line.
    This is a section of the full htaccess file and could be managed by a
    Section mixin.

    The Template mixin adds a method useful for processing a regular template
    file: apply_using(). It assumes that the file contains placeholder text to
    be replaced by actual data. The placeholders and actual data are passsed
    into the method as a dict. The resulting data is returned (presumably to be
    saved in another file.)

    The Parsable mixin adds a method useful for parsing (presumably)
    configuration files. It takes a dict of attribute names and regexes to be
    used. When setup_parsing() is called, a dynamic property is created for
    getting and setting a value in self.data based on the regex.

    :param atts: See notes in node.py

    Usage::

        >>> from ext_pylib.files import File

        >>> a_file = File({'path' : '/the/path/file', 'perms' : 0o600, 'owner' : 'root', 'group' : 'root'})
        >>> a_file.path
        '/the/path/file'

        >>> a_file.read()
        'The data...
    """

    def __init__(self, atts=None):
        """Initializes a new File instance."""
        super(File, self).__init__(atts)
        self.data = '' # Initialize data as an empty string.

    def __str__(self):
        """Returns a string with the path."""
        if not self.path:
            return '<file.File:stub>'
        return self.path

    def create(self, data=None):  # pylint: disable=arguments-differ
        """Creates the file/directory."""
        # pylint: disable=attribute-defined-outside-init
        if not self.path: # For stubs, just return True
            return True
        if self.exists():
            print(self.path + ' already exists.')
            if not prompt('Replace it?', False):
                return False
        print('Creating ' + self.path + '... ', end=' ')

        # Create parent directories
        if not self.parent_dir.exists():
            try:
                print('')
                self.parent_dir.create()
            except Exception as error:  # pylint: disable=broad-except
                print('[ERROR]')
                print(error)

        # Create the file
        try:
            file_handle = open(self.path, 'w')
            if data:  # If data was passed or data exists, write it.
                self.data = data
            if getattr(self, 'data', None):
                self.write(self.data, False, file_handle)
            file_handle.close()
            print('[OK]')
        except Exception as error:  # pylint: disable=broad-except
            print('[ERROR]')
            print(error)
            return False
        return all([self.chmod(), self.chown()])

    def remove(self, ask=True):  # pylint: disable=arguments-differ
        """Removes the file/directory."""
        if not self.path:
            return True
        if not self.exists():
            print(self.path + ' doesn\'t exist.')
            return True
        if not ask or prompt('Remove ' + self.path + '?'):
            os.remove(self.path)
            return True

    def read(self, flush_memory=False):
        """Returns the contents of the file.
           If the file doesn't exist, returns an empty string.

           Note that method first attempts to return the contents as in memory
           (which might differ from what is on disk)."""
        if flush_memory:  # Empty memory to force reading from disk
            self.data = ''
        if self.data != '':
            return self.data
        if not self.exists():  # If no data in memory and doesn't exist,
            self.data = ''     # return an empty string.
            return self.data
        try:  # Otherwise, try to read the file
            file_handle = open(self.path, 'r')
            self.data = file_handle.read()
            file_handle.close()
            return self.data
        except Exception:  # pylint: disable=broad-except
            print('[ERROR]')
            raise

    def readlines(self):
        """Returns the contents of the file as a list for iteration."""
        return self.read().split('\n')

    def write(self, data=None, append=True, handle=None):
        """Writes data to the file."""
        # pylint: disable=attribute-defined-outside-init
        if data:
            self.data = data  # Keep the data we're saving in memory.
        else:
            if self.data == '':
                raise UnboundLocalError('Must pass data to write method of File class.')
            else:
                data = self.data

        try:
            if handle: # When passed a handle, rely on the caller to open.close the file
                file_handle = handle
                file_handle.write(data)
            else:
                flags = 'a' if append else 'w'
                file_handle = open(self.path, flags)
                file_handle.write(data)
                file_handle.close()
            return True
        except Exception:  # pylint: disable=broad-except
            print('[ERROR]')
            return False

    def append(self, data, handle=None):
        """Appends the file with data. Just a wrapper."""
        return self.write(data, True, handle)

    def overwrite(self, data, handle=None):
        """Overwrites the file with data. Just a wrapper."""
        return self.write(data, False, handle)

    @Node.path.setter
    def path(self, path):
        """Sets the path."""
        # Check for None
        if path is None:
            return
        # File cannot end in '/'
        if path.endswith('/'):
            raise ValueError('"path" cannot end in "/" in a file.File class.')
        Node.path.fset(self, path)

    @property
    def parent_dir(self):
        """Returns a Dir instance representing the parent directory."""
        return Dir(self.parent_node.get_atts())


class Section(object):
    """A mixin class to work with a section template file.
    See Node class for atts to pass in at init.

    :param atts: See notes in node.py

    Usage::

        >>> from ext_pylib.files import File, Section

        >>> class SectionFile(Section, File): pass

        >>> a_file = SectionFile({'path' : '/the/path/file', 'perms' : 0o600, 'owner' : 'root', 'group' : 'root'})
        >>> a_file.is_applied(File({'path' : '/another/path/file'}).read())
        True
    """

    def is_applied(self, data):
        """Returns true if data has this section applied exactly."""
        return self.read() in data

    def is_in(self, data):
        """Returns true if data has the section, whether or not it is applied
        exactly."""
        # pylint: disable=attribute-defined-outside-init
        self._start_pos = data.find(self.start_section)
        self._end_pos = data.find(self.end_section)
        if self._start_pos < 0 and self._end_pos < 0:
            return False
        elif self._start_pos < self._end_pos:
            return True
        else:
            raise ValueError('Data passed to is_in() not formatted properly.')

    def apply_to(self, data, overwrite=False):
        """Returns a string in which the section is applied to the data."""
        if self.is_applied(data):
            return data
        if self.is_in(data):
            if overwrite:
                return data[:self._start_pos] + self.read() + '\n' + \
                        data[self._end_pos + len(self.end_section) + 1:]
            else:
                raise ValueError('[WARN] Section already exists, but overwrite flag was not set.')
        else:
            return data + '\n' + self.read() + '\n'

    @property
    def start_section(self):
        """Returns the string that denotes the start of the section."""
        if self.read() == '':
            raise EOFError('Section file has no data')
        return self.readlines()[0]

    @property
    def end_section(self):
        """Returns the string that denotes the end of the section."""
        if self.read() == '':
            raise EOFError('Section file has no data')
        lines = self.readlines()
        if len(lines) < 2:
            raise ValueError('Not a valid section file.')
        if lines[-1] != '':  # If the last line is blank, use the line before it.
            return lines[-1]
        return lines[-2]


class SectionFile(Section, File):
    """A File class implementing the Section Mixin."""


class Template(object):  # pylint: disable=too-few-public-methods
    """A mixin to work with a template file with placeholders.
    See Node class for atts to pass in at init.

    :param atts: See notes in node.py

    Usage::

        >>> from ext_pylib.files import File, Template

        >>> class TemplateFile(Template, File): pass

        >>> a_file = File({'path' : '/the/path/file', 'perms' : 0o600, 'owner' : 'root', 'group' : 'root'})
        >>> a_file.apply_using({'placeholder' : 'value'})
        The data...
    """

    def apply_using(self, placeholders):
        """Returns a string with placeholders replaced.
        Takes a dict of placeholders and values to replace."""
        data = self.read() # temp, throw-away (after returning) data value
        for placeholder, value in list(placeholders.items()):
            data = data.replace(placeholder, value)
        return data


class TemplateFile(Template, File):
    """A File class implementing the Template Mixin."""


class Parsable(object):
    """A mixin to be used with a File class to allow parsing.
    See Node class for atts to pass in at init.

    :param atts: See notes in node.py

    Usage::

        >>> from ext_pylib.files import File, Parsable

        >>> class ParsableFile(Parsable, File): pass

        >>> a_file = File({'path' : '/the/path/file', 'perms' : 0o600, 'owner' : 'root', 'group' : 'root'})
        >>> a_file.setup_parsing('htdocs' : 'DocumentRoot (.*)')

        >>> a_file.htdocs
        'example.com'
    """

    def setup_parsing(self, regexes=None):
        """Takes a dict of name:regex to parse self.data with.
           regex is either a string, a tuple of one, or a tuple of two with the
           second element being the regex mask used for assigning a new value
           to this property. It must contain '{}' to be the marker for the
           placeholder of the new value."""
        if not regexes:
            regexes = self.regexes
        for attribute, regex in regexes.items():
            att = getattr(self.__class__, attribute, None)
            if hasattr(self, attribute) and \
                not att.__class__.__name__ == 'DynamicProperty':
                raise AttributeError('Attribute "' + attribute + \
                                     '" already in use.')
            self.create_parseable_attr(attribute, regex)

    def create_parseable_attr(self, attribute, regex_tuple):
        """Creates a dynamic attribure on the Parsable class.
        This dynamically creates a property with a getter and setter. The regex
        is a closure. Each time the attribute is accessed, the regex is run
        against the data in memory. When the attribute is set to a new value,
        this value is changed in memory. file.write() must be called to write
        the changes to memory.

        NOTE: Because these are dynamic properties they are on the Class NOT
        the instance. This can cause difficult-to-find bugs when using the
        class with mulitple regexes and the same named attributes. Be sure to
        call setup_parsing() every time you change these regexes (expecially
        when changing to a regex/mask tuple or just a regex string).
        """
        if isinstance(regex_tuple, tuple):
            if len(regex_tuple) == 2:
                regex, mask = regex_tuple
            else:
                regex, mask = regex_tuple[0], '{}'
        else:
            regex, mask = regex_tuple, '{}'
        def getter_func(self):
            """Parsable dynamic attribute getter function."""
            results = re.findall(regex, self.read())
            if not results:
                return None
            elif len(results) == 1:
                return results[0]
            return results

        def setter_func(self, value):
            """Parsable dynamic attribute setter function.
            Note that this is only changing the value in memory.  You must call
            write()."""
            if not re.findall(regex, self.read()):
                # If the value doesn't exist, add it to the end of data
                self.data = self.data + '\n' + mask.format(value)
            else:  # otherwise just change it everywhere it exists
                self.data = re.sub(regex, mask.format(value), self.read())

        setdynattr(self, attribute, getter_func, setter_func)


class ParsableFile(Parsable, File):
    """A File class implementing the Parsable Mixin."""
