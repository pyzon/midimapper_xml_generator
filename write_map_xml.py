import os

from typing import List

from Param import Param
from channel_names import input_channel_names, aux_channel_names
from constants import INPUT_CHANNEL_RANGE, AUX_CHANNEL_RANGE
from read_csv import read_scale_csv


class ChannelType:
	def __init__(self, ch_range, name, sysex, name_list):
		self.channel_range = ch_range
		self.name = name
		self.sysex = sysex
		self.name_list = name_list


input_channel_type = ChannelType(INPUT_CHANNEL_RANGE, "IN", "03", input_channel_names)
aux_channel_type = ChannelType(AUX_CHANNEL_RANGE, "AUX", "05", aux_channel_names)


def write_map_xml(input_params, aux_params):
	input_channels_str = generate_general_channels_xml_part(input_params, input_channel_type)
	aux_channel_str = generate_general_channels_xml_part(aux_params, aux_channel_type)

	scales_str = generate_scales_xml_part()

	map_xml_str = f'<?xml version="1.0" encoding="UTF-8"?>'
	map_xml_str += f'\n<midimapconfig version="1.0">'
	map_xml_str += input_channels_str
	map_xml_str += aux_channel_str
	map_xml_str += scales_str
	map_xml_str += f'\n</midimapconfig>\n'

	map_xml = open("D:\\IT Projects\\Idea\\midimapper\\resources\\map.xml", "w")
	map_xml.write(map_xml_str)
	map_xml.close()


def generate_general_channels_xml_part(params: List[Param], channel_type: ChannelType):
	channels_str = ''
	for channel_id in channel_type.channel_range:
		local_channel_id = channel_id - channel_type.channel_range.start

		channel_number_str = '{:02x}'.format(local_channel_id)
		params_str = generate_params_xml_part(params)
		name = channel_type.name_list[local_channel_id]
		channel_str = f'\n\t<channel id="{channel_type.name}{local_channel_id + 1}" name="{name}">'
		channel_str += f'\n\t\t<address sysex0="{channel_type.sysex}" sysex1="{channel_number_str}" nrpn="{channel_id}"/>'
		channel_str += params_str
		channel_str += f'\n\t</channel>'
		channels_str += channel_str
	return channels_str


def generate_params_xml_part(params):
	params_str = ''
	for param in params:
		if param.scale == '':
			continue  # this is for development only
		data_str = f' bytes="{param.bytes}" scale="{param.scale}"'
		if param.signed != '':
			data_str += f' signed="{param.signed}"'
		if param.min != '':
			data_str += f' min="{param.min}"'
		if param.max != '':
			data_str += f' max="{param.max}"'
		if param.dmin != '':
			data_str += f' dmin="{param.dmin}"'
		if param.dmax != '':
			data_str += f' dmax="{param.dmax}"'
		if param.exp != '':
			data_str += f' exp="{param.exp}"'
		if param.thresh != '':
			data_str += f' thresh="{param.thresh}"'
		if param.base != '':
			data_str += f' base="{param.base}"'
		if param.coeff != '':
			data_str += f' coeff="{param.coeff}"'
		params_str += f'''
		<parameter name="{param.param_name}">
			<address sysex0="{param.sysex0}" sysex1="{param.sysex1}" nrpn="{param.nrpn}"/>
			<data{data_str}/>
		</parameter>'''
	return params_str


def generate_scales_xml_part():
	scales_str = ''
	files = os.listdir(os.getcwd())
	for file in files:
		if file.startswith('scale-') and file.endswith('.csv'):
			scale = read_scale_csv(file)
			scale_str = f'\n\t<scale id="{file[:-4]}">'
			for point in scale:
				scale_str += f'\n\t\t<point x="{point.x}" y="{point.y}"/>'
			scale_str += f'\n\t</scale>'
			scales_str += scale_str
	return scales_str
