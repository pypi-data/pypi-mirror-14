#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             user.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       01/13/2016
#

"""
ext_pylib.user.user
~~~~~~~~~~~~~~~~~~~

Functions for managing users.
"""

import grp
import os
import pwd

def get_current_username():
    """Returns the current username as a string."""
    return pwd.getpwuid(os.getuid()).pw_name

def get_current_groupname():
    """Returns the current groupname as a string."""
    return grp.getgrgid(os.getgid()).gr_name
