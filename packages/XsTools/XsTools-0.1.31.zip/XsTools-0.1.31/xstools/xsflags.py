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
This command-line program changes the configuration flags on an
XESS board like so:

    python xsflags.py -auxjtag on

which enables the auxiliary JTAG port on an XESS board
attached to a USB port and reports the result. For more info on
using this program, type xsflags -h.

This program was originally conceived and written in C++ by Dave
Vandenbout and then ported to python.
"""

try:
    import winsound
except ImportError:
    pass

import os
import sys
import string
from argparse import ArgumentParser
import xsboard as XSBOARD
import xserror as XSERROR
from __init__ import __version__

SUCCESS = 0
FAILURE = 1


def xsflags():

    try:
        num_boards = XSBOARD.XsUsb.get_num_xsusb()

        p = ArgumentParser(
            description='Change configuration flags on an XESS board.')

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
            choices=['xula-50','xula-200','xula2-lx9','xula2-lx25'])
        p.add_argument(
            '-j', '--jtag',
            type=str.lower,
            default='nochange',
            choices=['on', 'off'],
            help='Turn the auxiliary JTAG port on or off.')
        p.add_argument(
            '-f', '--flash',
            type=str.lower,
            default='nochange',
            choices=['on', 'off'],
            help=
            'Make the serial flash accessible to the FPGA. (Only applies to the XuLA-50 & XuLA-200 boards.)')
        p.add_argument(
            '-r', '--read',
            action='store_const',
            const=True,
            default=False,
            help='Read the flag settings from the XESS board.')
        p.add_argument(
            '-v', '--version',
            action='version',
            version='%(prog)s ' + __version__,
            help='Print the version number of this program and exit.')
            
        args = p.parse_args()

        if num_boards > 0:

            xs_board = XSBOARD.XsBoard.get_xsboard(args.usb, args.board)

            try:
                if args.jtag == 'on':
                    xs_board.set_aux_jtag_flag(True)
                elif args.jtag == 'off':
                    xs_board.set_aux_jtag_flag(False)

                if args.flash == 'on':
                    xs_board.set_flash_flag(True)
                elif args.flash == 'off':
                    xs_board.set_flash_flag(False)

                flag = xs_board.get_aux_jtag_flag()
                print 'Auxiliary JTAG port is ' + (
                    (flag == True and 'enabled.') or
                    (flag == False and 'disabled.'))
                flag = xs_board.get_flash_flag()
                print 'Serial flash is ' + (
                    (flag == True and 'enabled.') or
                    (flag == False and 'disabled.'))

            except XSERROR.XsError as e:
                pass

        else:
            XSERROR.XsFatalError("No XESS Boards found!")

        sys.exit(SUCCESS)
        
    except SystemExit as e:
        os._exit(SUCCESS)


if __name__ == '__main__':
    xsflags()
