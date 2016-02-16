from __future__ import division

__author__ = 'Flynston'
__license__ = 'WTFPL'

import base64

from .gui.structures import ItemList


class VPNserver:
	def __init__(self, country, ip, speed, 
				ping, sessions, score, vpn_config):
		
		self.country = country
		self.ip = ip
		self._speed = int(speed)
		self.ping = ping
		self.sessions = sessions
		self.score = score
		self.vpn_config = vpn_config
	
	@property
	def speed(self):
		return self._speed / (1024 * 1024)


class VPNiterator:
	
	def __init__(self, response):
		'''
		VPNiterator gets raw response string and represents 
		simple generator which yields VPNserver objects

		Arguments:
		response -- response raw string
		'''
		self.response = response
		self._parse_response()
		self.iterator = (self._create_VPN(row) for row in self.vpn_data_rows[2:-2])

	def _parse_response(self):
		'''fetches servers info rows and labels of data columns'''
		self.vpn_data_rows = self.response.replace('\r','').split('\n')
		labels = self.vpn_data_rows[1].split(',')
		self.labels_dict = { label: num for num, label in enumerate(labels) }
	
	def _create_VPN(self, data_row):
		'''
		converts raw server info string to VPNserver object

		Arguments:
		data_row -- server info string
		'''
		data_row=data_row.split(',')
		country = data_row[self.labels_dict['CountryLong']]
		ip = data_row[self.labels_dict['IP']]
		speed = data_row[self.labels_dict['Speed']]
		ping = data_row[self.labels_dict['Ping']]
		sessions = data_row[self.labels_dict['NumVpnSessions']]
		score = data_row[self.labels_dict['Score']]
		base64_info = data_row[self.labels_dict['OpenVPN_ConfigData_Base64']]	
		vpn_config = base64.b64decode(base64_info)

		return VPNserver(country, ip, speed, ping,
						sessions, score, vpn_config)
		

	def __iter__(self):
		return self.iterator	

	def next(self):
		return self.iterator.next()	
		

tcp_list = []
udp_list = []
	
def parse(vpn_data):
	
	vpn_iterator = VPNiterator(vpn_data)
	for vpn in vpn_iterator:
		if b'proto tcp' in vpn.vpn_config:
			tcp_list.append(vpn)
		else:
			udp_list.append(vpn)
	
	protocols_list = create_protocols_list()
	return protocols_list

def create_protocols_list():
	global tcp_list, udp_list

	protocols_list = ItemList()
	tcp_country_list = create_country_list(tcp_list)
	udp_country_list = create_country_list(udp_list)

	protocols_list.item_list = [("tcp",len(tcp_list)),("udp",len(udp_list))]
	protocols_list.item_map = {
						"tcp": tcp_country_list,
						"udp": udp_country_list
						}

	return protocols_list

def create_country_list(vpn_list):
	country_list = ItemList()
	country_vpn_map = {}	
	for vpn in vpn_list:
		if country_vpn_map.get(vpn.country):
			country_vpn_map.get(vpn.country).append(vpn)
		else:
			country_vpn_map[vpn.country] = [vpn]
		
	country_list.item_map = { 
		country: create_ip_list(vpn_list) 
		for country, vpn_list in country_vpn_map.items()
	}

	country_list.item_list = [(country, len(vpn_list))
			for country, vpn_list in country_vpn_map.items()
	]

	country_list.item_list.sort(key=lambda tup: tup[1], reverse=True)

	return country_list

def create_ip_list(vpn_list):
	ip_list = ItemList()

	vpn_list.sort(key=lambda vpn: vpn.score, reverse=True)	

	ip_list.item_list = [(vpn.ip, vpn.speed) for vpn in vpn_list]
	ip_list.item_map = {vpn.ip: vpn for vpn in vpn_list}

	return ip_list
