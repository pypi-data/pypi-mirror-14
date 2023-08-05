#!/usr/bin/python
# -*- coding: utf-8 -*-

# **********************************************************************
#   This program is free software; you can redistribute it and/or
#   modify it under the terms of the GNU General Public License
#   as published by the Free Software Foundation; either version 2
#   of the License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
#   02111-1307, USA.
#
#   (c)2012 - X Engineering Software Systems Corp. (www.xess.com)
# **********************************************************************
"""
This command-line program runs a self-test on an XESS board like so:

    python xstest.py

which downloads a self-test bitstream into an XESS board
attached to a USB port and reports the result. For more info on
using this program, type xstest -h.

This program was originally conceived and written in C++ by Dave
Vandenbout and then ported to python.
"""

try:
    import winsound
except ImportError:
    pass

import sys
import os
import string
from argparse import ArgumentParser
import xsboard as XSBOARD
import xserror as XSERROR
from __init__ import __version__

SUCCESS = 0
FAILURE = 1


def xstest():

    try:
        num_boards = XSBOARD.XsUsb.get_num_xsusb()

        p = ArgumentParser(description='Run self-test on an XESS board.')

        p.add_argument(
            '-u', '--usb',
            type=int,
            default=0,
            choices=range(num_boards),
            help=
            'The USB port number for the XESS board. If you only have one board, then use 0.')
        p.add_argument(
            '-b', '--board',
            type=str.lower,
            default='none',
            choices=['xula-50', 'xula-200', 'xula2-lx9', 'xula2-lx25'])
        p.add_argument(
            '-m', '--multiple',
            action='store_const',
            const=True,
            default=False,
            help=
            'Run the self-test each time a board is detected on the USB port.')
        p.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s ' + __version__,
            help='Print the version number of this program and exit.')
            
        args = p.parse_args()

        while (True):
            num_boards = XSBOARD.XsUsb.get_num_xsusb()
            if num_boards > 0:
                xs_board = XSBOARD.XsBoard.get_xsboard(args.usb, args.board)
                try:
                    xs_board.do_self_test()
                except XSERROR.XsError as e:
                    try:
                        winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
                    except:
                        pass
                    if args.multiple:
                        xs_board.xsusb.disconnect()
                        while XSBOARD.XsUsb.get_num_xsusb() != 0:
                            pass
                        continue
                    else:
                        sys.exit(FAILURE)
                print "Success:", xs_board.name, "passed diagnostic test!"
                try:
                    winsound.MessageBeep()
                except:
                    pass
                if args.multiple:
                    xs_board.xsusb.disconnect()
                    while XSBOARD.XsUsb.get_num_xsusb() != 0:
                        pass
                    continue
                else:
                    sys.exit(SUCCESS)
            elif not args.multiple:
                XSERROR.XsFatalError("No XESS Boards found!")

    except SystemExit as e:
        os._exit(SUCCESS)


if __name__ == '__main__':
    xstest()
