#!/usr/bin/env python

__author__ = 'Flynston'
__license__ = 'WTFPL'

from vpnfetch.gui import ui

from curses import wrapper

if __name__ == '__main__':
	wrapper(ui.main)
