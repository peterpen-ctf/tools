
from collections import namedtuple
from io import open

Action = namedtuple("Action", ["key","state"])

PROTO_STATE = 0
COUNTRY_STATE = 1
IP_STATE = 2

def get_proto_list(dm):
	return dm.proto_list

def get_country_list(dm):
	return dm.country_list

def get_ip_list(dm):
	return dm.ip_list

def to_proto_state(dm):
	dm.current_state = PROTO_STATE
	dm.active_window = dm.ui.left_window
	
	dm.title_list = [dm.title_list[0]]	
	dm.ui.title_bar.set_title(dm.title_list)
	

def redraw_proto_state(dm):
	
	dm.ui.left_window.set_list(dm.proto_list)
	dm.ui.right_window.set_list(dm.country_list)
	
	dm.ui.info_bar.set_info(None)
	dm.ui.title_bar.set_title(dm.title_list)

def up_proto_state(dm):

	new_highlight = up_list_node(dm.proto_list)

	new_protocol = dm.proto_list.item_list[new_highlight][0]
	dm.title_list[0] = new_protocol
	dm.country_list = dm.proto_list.item_map[new_protocol]
	
	dm.ui.left_window.set_list(dm.proto_list)
	dm.ui.right_window.set_list(dm.country_list)
	dm.ui.title_bar.set_title(dm.title_list)

def down_proto_state(dm):
	
	new_highlight = down_list_node(dm.proto_list)
	
	new_protocol = dm.proto_list.item_list[new_highlight][0]
	dm.title_list[0] = new_protocol
	dm.country_list = dm.proto_list.item_map[new_protocol]

	dm.ui.left_window.set_list(dm.proto_list)
	dm.ui.right_window.set_list(dm.country_list)
	dm.ui.title_bar.set_title(dm.title_list)


def to_country_state(dm):
	dm.current_state = COUNTRY_STATE
	dm.active_window = dm.ui.right_window
	
	dm.ui.left_window.set_list(dm.proto_list)
	dm.ui.right_window.set_list(dm.country_list)
	
	if len(dm.title_list) > 2: 
		dm.title_list = dm.title_list[:2]
	else:
		cur_country = dm.country_list.item_list[dm.country_list.highlighted][0]
		dm.title_list.append(cur_country)
	
	dm.ui.info_bar.set_info(None)
	try:
		dm.ui.title_bar.set_title(dm.title_list)
	except:
		raise Exception ("title_list = {}".format(dm.title_list))

def redraw_country_state(dm):

	dm.ui.left_window.set_list(dm.proto_list)
	dm.ui.right_window.set_list(dm.country_list)

	dm.ui.info_bar.set_info(None)
	dm.ui.title_bar.set_title(dm.title_list)


def down_country_state(dm):

	new_highlight = down_list_node(dm.country_list)

	new_country = dm.country_list.item_list[new_highlight][0]
	dm.ip_list = dm.country_list.item_map[new_country]
	dm.title_list[1] = new_country

	dm.ui.right_window.set_list(dm.country_list)
	dm.ui.title_bar.set_title(dm.title_list)

def up_country_state(dm):

	new_highlight = up_list_node(dm.country_list)

	new_country = dm.country_list.item_list[new_highlight][0]
	dm.ip_list = dm.country_list.item_map[new_country]
	dm.title_list[1] = new_country

	dm.ui.right_window.set_list(dm.country_list)
	dm.ui.title_bar.set_title(dm.title_list)


def to_ip_state(dm):
	dm.current_state = IP_STATE

	dm.ui.left_window.set_list(dm.country_list)
	dm.ui.right_window.set_list(dm.ip_list)

	cur_highlight = dm.ip_list.highlighted
	cur_ip = dm.ip_list.item_list[cur_highlight][0]
	dm.title_list.append(cur_ip)	

	vpn = dm.ip_list.item_map[cur_ip]

	dm.ui.info_bar.set_info([vpn.speed,vpn.ping,vpn.sessions])
	dm.ui.title_bar.set_title(dm.title_list)

def redraw_ip_state(dm):
	dm.ui.title_bar.set_title(["redrawn title"])

	dm.ui.left_window.set_list(dm.country_list)
	dm.ui.right_window.set_list(dm.ip_list)

	cur_highlight = dm.ip_list.highlighted
	cur_ip = dm.ip_list.item_list[cur_highlight][0]	

	vpn = dm.ip_list.item_map[cur_ip]

	dm.ui.info_bar.set_info([vpn.speed,vpn.ping,vpn.sessions])
	dm.ui.title_bar.set_title(dm.title_list)


def down_ip_state(dm):
	
	new_highlight = down_list_node(dm.ip_list)

	new_ip = dm.ip_list.item_list[new_highlight][0]
	dm.title_list[2]=new_ip

	vpn = dm.ip_list.item_map[new_ip]

	dm.ui.right_window.set_list(dm.ip_list)
	dm.ui.info_bar.set_info([vpn.speed,vpn.ping,vpn.sessions])
	dm.ui.title_bar.set_title(dm.title_list)

def up_ip_state(dm):
	
	new_highlight = up_list_node(dm.ip_list)

	new_ip = dm.ip_list.item_list[new_highlight][0]
	dm.title_list[2]=new_ip

	vpn = dm.ip_list.item_map[new_ip]

	dm.ui.right_window.set_list(dm.ip_list)
	dm.ui.info_bar.set_info([vpn.speed,vpn.ping,vpn.sessions])
	dm.ui.title_bar.set_title(dm.title_list)

def down_list_node(node):
	cur_highlight = node.highlighted
	list_len = len(node.item_list)
	new_highlight = cur_highlight+1 if cur_highlight < list_len-1 else cur_highlight
	node.highlighted = new_highlight

	return new_highlight

def up_list_node(node):
	cur_highlight = node.highlighted
	new_highlight = cur_highlight-1 if cur_highlight > 0 else 0
	node.highlighted = new_highlight

	return	new_highlight

def scroll_up_list(node):
	node.highlighted = 0

def scroll_down_list(node):
	node.highlighted = len(node.item_list)-1

def save_vpn_config(dm):
	
	cur_highlight = dm.ip_list.highlighted
	cur_ip = dm.ip_list.item_list[cur_highlight][0]
	
	vpn = dm.ip_list.item_map[cur_ip]
	file_name = "vpn_{}_{}.ovpn".format(vpn.country.replace(' ','_'), vpn.ip)
	try:
		with open(file_name, "wb") as f:
			f.write(vpn.vpn_config)
			dm.ui.info_bar.set_title("vpn config successfully saved!")
	except IOError:
			dm.ui.info_bar.set_title("failed to save file!")	
