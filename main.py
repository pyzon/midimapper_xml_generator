import csv
import os
from dataclasses import dataclass


@dataclass
class Param:
	param_name: str
	sysex0: str
	sysex1: str
	nrpn: str
	bytes: str
	scale: str
	signed: str
	min: str
	max: str
	dmin: str
	dmax: str
	exp: str
	thresh: str
	base: str
	coeff: str
	control: str


@dataclass
class Point:
	x: str
	y: str


def main():
	input_params = read_input_csv()
	input_params_str = generate_params_xml_part(input_params)

	scales_str = generate_scales_xml_part()

	map_xml_str = f'''<?xml version="1.0" encoding="UTF-8"?>
<midimapconfig version="1.0">
	<channel id="CH1" name="Kick out">
		<address sysex0="03" sysex1="00" nrpn="00"/>{input_params_str}
	</channel>
	<channel id="CH2" name="Kick in">
		<address sysex0="03" sysex1="01" nrpn="01"/>
		<parameter name="phase">
			<address sysex0="00" sysex1="09" nrpn="00"/>
			<data min="0" max="1" bytes="1" signed="false" scale="LIN" dmin="0" dmax="1"/>
		</parameter>
	</channel>{scales_str}
</midimapconfig>'''

	map_xml = open("D:\\IT Projects\\Idea\\midimapper\\resources\\map.xml", "w")
	map_xml.write(map_xml_str)
	map_xml.close()

	# Write remote_setup.xml
	ctrls = ''
	entries = ''
	for param in input_params:
		if param.scale == '':
			continue

		nrpn = int(param.nrpn, base=16)
		ctrls += f'\n<ctrl><name>CH1 {param.param_name}</name><stat>2</stat><chan>0</chan>'
		ctrls += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
		entries += f'\n<entry ctrl="CH1 {param.param_name}">'
		entries += f'\n<value><device>VST Mixer</device><chan>0</chan><name>{param.control}</name><flags>0</flags></value>'
		entries += f'\n</entry>'

	remote_setup_str = f'''<?xml version="1.0" encoding="UTF-8"?>
<remotedescription version="1.1">
<ctrltable name="Standard MIDI">{ctrls}
</ctrltable>
<bank name="VST 1-16">{entries}
</bank>
</remotedescription>
'''

	remote_setup_xml = open("D:\\IT Projects\\Idea\\midimapper\\resources\\remote_setup.xml", "w")
	remote_setup_xml.write(remote_setup_str)
	remote_setup_xml.close()


def read_input_csv():
	params = []
	with open('input.csv') as input_csv:
		reader = csv.reader(input_csv)
		for row in reader:
			params.append(Param(
				row[0],
				row[1],
				row[2],
				row[3],
				row[4],
				row[5],
				row[6],
				row[7],
				row[8],
				row[9],
				row[10],
				row[11],
				row[12],
				row[13],
				row[14],
				row[15],
			))
	return params[1:]


def generate_params_xml_part(params):
	params_str = ''
	for param in params:
		if param.scale == '':
			continue
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


def read_scale_csv(file):
	scale = []
	with open(file) as scale_csv:
		reader = csv.reader(scale_csv)
		for row in reader:
			scale.append(Point(
				row[0],
				row[1]
			))
	return scale[1:]


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


if __name__ == '__main__':
	main()
