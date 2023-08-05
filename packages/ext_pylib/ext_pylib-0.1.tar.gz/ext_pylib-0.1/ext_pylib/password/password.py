#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             password.py
# maintainer:       Harold Bradley III
# email:            harold@bradleystudio.net
#

"""
ext_pylib.password.password
~~~~~~~~~~~~~~~~~~~~~~~~~~~

A module to create passwords.
"""

from random import choice


# Defines the default characters for use in generating a password
DEFAULT_CHAR_SET = {
    'small': 'abcdefghijklmnopqrstuvwxyz',
    'nums': '0123456789',
    'big': 'ABCDEFGHIJKLMNOPQRSTUVWXYZ',
    'special': '^!$%&=?{[]}+~#-_.:,;<>|'
}

def generate_pw(length=18, char_set=None):
    """Generates a pseudo-randomly generated password and returns it as a string.
    Adapted from: http://code.activestate.com/recipes/578169-extremely-strong-password-generator/"""
    char_set = char_set or DEFAULT_CHAR_SET
    password = []

    while len(password) < length:
        subset = choice(list(char_set.keys()))  # Get a random subset of characters
                                                # from which to choose
        # Ensure it isn't the same subset as the previous character in the password.
        if password and password[-1] in char_set[subset]:
            continue
        else:
            password.append(choice(char_set[subset]))

    return ''.join(password)
