import sys
import curses

def quit(ui):
	curses.endwin()
	sys.exit(0)

def quit_error(ui, code):
	curses.endwin()
	sys.exit(code)

def left_key(ui):
	ui.data_manager.pressed_key('left')

def right_key(ui):
	ui.data_manager.pressed_key('right')

def down_key(ui):
	ui.data_manager.pressed_key('down')

def up_key(ui):
	ui.data_manager.pressed_key('up')

def enter_key(ui):
	ui.data_manager.pressed_key('enter')

def g_big_key(ui):
	ui.data_manager.scroll_list('G')

def g_small_key(ui):
	ui.data_manager.scroll_list('g')

def resize_terminal(ui):
	ui.init_windows()
	ui.data_manager.resize_terminal()
