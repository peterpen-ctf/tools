
import sys
import curses

from . import action
from . import widgets

from curses import wrapper

from .data_manager import DataManager

NEWLINE = 10
CARRIAGE_RETURN = 13

key_bind_action = {
            ord('q'): action.quit,
            curses.KEY_LEFT: action.left_key,
			curses.KEY_RIGHT: action.right_key,
			curses.KEY_DOWN: action.down_key,
			curses.KEY_UP: action.up_key,
			ord('h'): action.left_key,
			ord('l'): action.right_key,
			ord('j'): action.down_key,
			ord('k'): action.up_key,
			ord('G'): action.g_big_key,
			ord('g'): action.g_small_key,
			curses.KEY_ENTER: action.enter_key,
			NEWLINE: action.enter_key,
			CARRIAGE_RETURN: action.enter_key,
			curses.KEY_RESIZE: action.resize_terminal	
            }


class UI:
	stdscr = None
	def __init__(self, stdscr):
		self.stdscr = stdscr
		self.init_curses()
		
		self.data_manager = DataManager(self)
		
		self.init_windows()
		self.data_manager.init_ui()

	def init_curses(self):
		self.stdscr.refresh()
		
		curses.use_default_colors()
		self.max_y, self.max_x = self.stdscr.getmaxyx()

		curses.noecho()
		curses.cbreak()
	
		curses.curs_set(0)
		self.stdscr.keypad(1)
	
	def init_windows(self):
		self.stdscr.erase()
		self.stdscr.refresh()
	
		self.title_bar = widgets.TitleBar(1, self.max_x);
		self.info_bar = widgets.InfoBar(1, self.max_x, self.max_y-1, 0)
		self.left_window = widgets.Window(self.max_y-2,int(0.3*self.max_x),1,0)
		self.right_window = widgets.Window(self.max_y-2,self.max_x-int(0.3*self.max_x),1, int(0.3*self.max_x)+1)
	

	def loop(self):
		while True:
			ch = self.stdscr.getch()
			key_action = key_bind_action.get(ch, None)
			if key_action:
				key_action(self)
	
	def show_message(self, show_message):
		self.stdscr.erase()
		self.stdscr.addstr(self.max_y//2, (self.max_x-len(show_message))//2, show_message)
		self.stdscr.refresh()
	
	def quit_error(self, err_message):
		self.show_message(err_message)
		self.stdscr.getch()
		action.quit_error(self, 1)

		
def main(stdscr):
	ui = UI(stdscr)
	ui.loop()

