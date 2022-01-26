from constants import INPUT_CHANNEL_RANGE, MAX_CHANNELS_PER_BANK


def write_remote_setup_xml(input_params):
	ctrls = ''

	entry_index_in_bank = 0
	entries_in_bank = ''
	all_entries = []

	for channel_id in INPUT_CHANNEL_RANGE:  # channel_id is the global id throughout all types of channels
		input_channel_id = channel_id - INPUT_CHANNEL_RANGE.start  # local id, used in the name of the channel

		if entry_index_in_bank == MAX_CHANNELS_PER_BANK:
			entry_index_in_bank = 0
			all_entries.append(entries_in_bank)
			entries_in_bank = ''

		for param in input_params:
			if param.scale == '':
				continue

			nrpn = int(param.nrpn) + channel_id * 128
			ctrls += f'\n<ctrl><name>IN{input_channel_id} {param.param_name}</name><stat>2</stat><chan>0</chan>'
			ctrls += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
			entries_in_bank += f'\n<entry ctrl="IN{input_channel_id} {param.param_name}">'
			entries_in_bank += f'\n<value><device>VST Mixer</device><chan>{channel_id}</chan>'
			entries_in_bank += f'<name>{param.control}</name><flags>0</flags></value>'
			entries_in_bank += f'\n</entry>'

		entry_index_in_bank += 1

	# adding the rest of entries
	all_entries.append(entries_in_bank)

	remote_setup_str = f'<?xml version="1.0" encoding="UTF-8"?>'
	remote_setup_str += f'\n<remotedescription version="1.1">'
	remote_setup_str += f'\n<ctrltable name="Standard MIDI">{ctrls}'
	remote_setup_str += f'\n</ctrltable>'
	for bank_id, entries in enumerate(all_entries):
		start = bank_id * MAX_CHANNELS_PER_BANK + 1
		end = (bank_id + 1) * MAX_CHANNELS_PER_BANK
		remote_setup_str += f'\n<bank name="VST {start}-{end}">{entries}'
		remote_setup_str += f'\n</bank>'
	remote_setup_str += f'\n</remotedescription>\n'

	remote_setup_xml = open("D:\\IT Projects\\Idea\\midimapper\\resources\\remote_setup.xml", "w")
	remote_setup_xml.write(remote_setup_str)
	remote_setup_xml.close()
