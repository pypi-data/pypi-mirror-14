#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
ext_pylib.input
~~~~~~~~~~~~~~~~

Functions for displaying and handling input on the terminal.
"""

from __future__ import absolute_import

# Use Python 2 input unless raw_input doesn't exist
try:
    INPUT = raw_input
except NameError:
    INPUT = input

# pylint: disable=wrong-import-position
# this import MUST be after INPUT is defined
from .prompts import prompt, prompt_str, warn_prompt
