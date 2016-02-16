
import curses

from . import structures

class Widget:
	
	def create_window(self, height, width,
					begin_y, begin_x):
		self.begin_x = begin_x
		self.begin_y = begin_y
		self.height = height
		self.width = width
		self.win = curses.newwin(self.height, self.width,
								self.begin_y, self.begin_x)

	def refresh(self):
		self.win.refresh()

class TitleBar(Widget):
	
	def __init__(self, height, width):
		self.create_window(height,width,0,0)
	
	def set_title(self, args):
		if len(args) > 2:
			args[2] = args[2].ljust(15)
		str_arg = ' -> '.join(args[:-1])+' -> '
		
		color_arg = args[-1]

		width_margin = int(0.3*self.width)

		text_width = self.width - width_margin - 3
		if len(str_arg+color_arg) > text_width:
			left_width = text_width-len(color_arg)
			str_arg = '~'+str_arg[-left_width:]	
		
		

		self.win.erase()	
		self.win.addstr(self.height//2, width_margin+1, str_arg)
		self.win.addstr(self.height//2, width_margin+len(str_arg)+1, 
										color_arg, curses.A_BOLD)
		self.win.refresh()

info_short = {
			'speed':'sp',
			'ping':'p',
			'sessions':'ses'
			}

class InfoBar(Widget):

	def __init__(self, height, width, begin_y, begin_x):
		self.create_window(height, width, begin_y, begin_x)

	def set_info(self, args=None):
		self.win.erase()
		if not args:
			self.win.refresh()
			return
	
		small_width = 60
	
		speed_title = 'speed' if self.width > small_width else info_short['speed']
		ping_title = 'ping' if self.width > small_width else info_short['ping']
		session_title = 'sessions' if self.width > small_width else info_short['sessions']	

		step = int(0.3*self.width)
		
		self.win.addstr(self.height//2, 1, 
						"{}:{:>5.2f}Mbps".format(speed_title, args[0]))

		self.win.addstr(self.height//2, step+5,
						"{}:{:>2}ms".format(ping_title, args[1]))

		self.win.addstr(self.height//2, step*2+5,
						"{}: {}".format(session_title, args[2]))
		self.win.refresh()
				
	def set_title(self, message):
		self.win.erase()
		self.win.addstr(self.height//2,3, message)
		self.win.refresh()

class Window(Widget):

	def __init__(self, height, width, begin_y, begin_x):
		self.create_window(height, width, begin_y, begin_x)

	def set_list(self, node):
		self.win.erase()
		highlighted = node.highlighted
		
		if not node.item_list:
			no_data_str = "no VPN data"
			self.win.addstr(self.height//2,(self.width-len(no_data_str))//2,
								no_data_str)
			self.win.refresh()
			return

		list_len = len(node.item_list)
		half_win_height = self.height//2

		if highlighted < half_win_height or list_len < self.height:
			left = 0
			right = min(list_len, self.height)
		elif highlighted + half_win_height < list_len:
			left = highlighted - half_win_height
			right = highlighted + half_win_height
		else:
			left = list_len - self.height
			right = min(highlighted + half_win_height, list_len)		

		for index in range(left, right):
			try:
				item = node.item_list[index]
			except IndexError:
				self.win.addstr("Index out of range!")
				break
			text_atr = curses.A_REVERSE if index == highlighted else curses.A_NORMAL
			left_str = str(item[0])
			if isinstance(item[1], int):
				right_str = str(item[1])
			else:
				right_str = "{:.2f}".format(item[1])

			left_str = left_str if len(left_str)+len(right_str) < self.width else left_str[:self.width-len(right_str)-3]+'~'
			left_str = left_str.ljust(self.width-len(right_str)-1)	
			item_str = "{}{}".format(left_str, right_str) 
			self.win.addstr(index-left, 0, item_str, text_atr)
		
		self.win.refresh()	
	
