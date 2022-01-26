import os
from read_csv import read_scale_csv
from constants import INPUT_CHANNEL_COUNT, INPUT_PARAM_COUNT, INPUT_CHANNEL_RANGE


def write_map_xml(input_params):
	input_channels_str = generate_input_channels_xml_part(input_params)

	scales_str = generate_scales_xml_part()

	map_xml_str = f'<?xml version="1.0" encoding="UTF-8"?>'
	map_xml_str += f'\n<midimapconfig version="1.0">{input_channels_str}{scales_str}'
	map_xml_str += f'\n</midimapconfig>\n'

	map_xml = open("D:\\IT Projects\\Idea\\midimapper\\resources\\map.xml", "w")
	map_xml.write(map_xml_str)
	map_xml.close()


def generate_input_channels_xml_part(params):
	channels_str = ''
	for channel_id in INPUT_CHANNEL_RANGE:
		channel_number_str = '{:02x}'.format(channel_id)
		input_params_str = generate_input_params_xml_part(params)
		channel_str = f'\n\t<channel id="IN1" name="Kick out">'
		channel_str += f'\n\t\t<address sysex0="03" sysex1="{channel_number_str}" nrpn="{channel_id}"/>'
		channel_str += input_params_str
		channel_str += f'\n\t</channel>'
		channels_str += channel_str
	return channels_str


def generate_input_params_xml_part(params):
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
