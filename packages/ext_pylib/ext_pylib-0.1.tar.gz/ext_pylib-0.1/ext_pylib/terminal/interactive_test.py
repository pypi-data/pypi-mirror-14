#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# name:             interactive_test.py
# author:           Harold Bradley III
# email:            harold@bradleystudio.net
# created on:       02/26/2016
#

"""
ext_pylib.terminal.interactive_test
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This module is just an interactive test for the ansi and colors modules.
"""

from __future__ import absolute_import

from timeit import timeit

from ext_pylib.terminal import ansi, colors

def main():
    """The main test suite."""
    ansi.reset()

    print('ext_pylib interactive terminal test')
    ansi.cursor_down(2)

    print('Testing colors...')
    print('Row 1:  | Row 2:   | ')
    print(colors.black_on_red('black'))
    print(colors.red('red'))
    print(colors.green('green'))
    print(colors.yellow('yellow'))
    print(colors.blue('blue'))
    print(colors.magenta('magenta'))
    print(colors.cyan('cyan'))
    print(colors.white('white'))

    ansi.cursor_up(8)
    ansi.cursor_right(10)

    print(colors.black_on_white('black'))
    ansi.cursor_right(10)
    print(colors.red_on_black('red'))
    ansi.cursor_right(10)
    print(colors.green_on_red('green'))
    ansi.cursor_right(10)
    print(colors.yellow_on_green('yellow'))
    ansi.cursor_right(10)
    print(colors.blue_on_yellow('blue'))
    ansi.cursor_right(10)
    print(colors.magenta_on_blue('magenta'))
    ansi.cursor_right(10)
    print(colors.cyan_on_magenta('cyan'))
    ansi.cursor_right(10)
    print(colors.white_on_cyan('white'))

    print('\n')
    print(colors.underline(colors.red('This is red text that is underlined')))
    print(colors.bold(colors.green('This is green text that is bold')))
    print(colors.reverse(colors.green_on_blue('This is green on blue text that is reversed')))

if __name__ == '__main__':
    print(timeit(main, number=1))
