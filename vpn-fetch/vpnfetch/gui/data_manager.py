
from io import open

from .. import vpn_parser 
from . import states
from .states import Action


VPN_GATE_URL='http://www.vpngate.net/api/iphone/'

states_map = {

	Action('right', states.PROTO_STATE): states.to_country_state,
	Action('enter', states.PROTO_STATE): states.to_country_state,
    Action('down', states.PROTO_STATE): states.down_proto_state,
    Action('up', states.PROTO_STATE): states.up_proto_state,

    Action('left', states.COUNTRY_STATE): states.to_proto_state,
    Action('right', states.COUNTRY_STATE): states.to_ip_state,
	Action('enter', states.COUNTRY_STATE): states.to_ip_state,
    Action('down', states.COUNTRY_STATE): states.down_country_state,
    Action('up', states.COUNTRY_STATE): states.up_country_state,
	
	Action('left', states.IP_STATE): states.to_country_state,
	Action('enter', states.IP_STATE): states.save_vpn_config,
    Action('down', states.IP_STATE): states.down_ip_state,
    Action('up', states.IP_STATE): states.up_ip_state,

}

redraw_map = {

	states.PROTO_STATE: states.redraw_proto_state,
	states.COUNTRY_STATE: states.redraw_country_state,
	states.IP_STATE: states.redraw_ip_state

}

list_map = {

	states.PROTO_STATE: states.get_proto_list,
	states.COUNTRY_STATE: states.get_country_list,
	states.IP_STATE: states.get_ip_list

}

scroll_map = {
	'G': states.scroll_down_list,
	'g': states.scroll_up_list
}

class DataManager:
	
	def __init__(self, ui):
		self.ui = ui
		self.__download_vpn_list()
	
		self.proto_list = vpn_parser.parse(self.vpn_data)
		self.country_list = self.proto_list.item_map["tcp"]
		
		first_country = self.country_list.item_list[0][0]
		self.title_list = ["tcp", first_country]	
		self.ip_list = self.country_list.item_map[first_country]
	
	def init_ui(self):
		self.ui.title_bar.set_title(self.title_list)
		self.ui.info_bar.set_info(None)

		self.ui.left_window.set_list(self.proto_list)
		self.ui.right_window.set_list(self.country_list) 
		self.active_window = self.ui.right_window

		self.current_state = states.COUNTRY_STATE
		
	
	def __download_vpn_list(self):
		self.vpn_data = None
		try:
			self.ui.show_message("Fetching VPN list...")
			import requests
			self.vpn_data = requests.get(VPN_GATE_URL).text
		except ImportError as e:
			self.ui.quit_error("failed to import requests")
		except IOError as e:
			self.ui.quit_error("failed to fetch vpn server list")
	
	
	def pressed_key(self, key_string):

		action = states_map.get(
				Action(key=key_string, state=self.current_state), None)
		if action:
			action(self)

	def scroll_list(self, key_string):		
		action = scroll_map.get(key_string, None)
		if action:
			cur_list_extract = list_map.get(self.current_state, None)
			list_node = cur_list_extract(self) if cur_list_extract else None
			if list_node:
				action(list_node)
				self.active_window.set_list(list_node)	

	def resize_terminal(self):
		action = redraw_map.get(self.current_state, None)
		if action:
			action(self)


