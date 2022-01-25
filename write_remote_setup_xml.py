from constants import CHANNEL_COUNT


def write_remote_setup_xml(input_params):
	ctrls = ''
	entries = ''
	for channel_id in range(CHANNEL_COUNT):
		for param in input_params:
			if param.scale == '':
				continue

			nrpn = int(param.nrpn, base=16)
			ctrls += f'\n<ctrl><name>CH{channel_id} {param.param_name}</name><stat>2</stat><chan>0</chan>'
			ctrls += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
			entries += f'\n<entry ctrl="CH{channel_id} {param.param_name}">'
			entries += f'\n<value><device>VST Mixer</device><chan>{channel_id}</chan>'
			entries += f'<name>{param.control}</name><flags>0</flags></value>'
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
