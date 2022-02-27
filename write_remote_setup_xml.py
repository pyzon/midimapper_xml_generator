from constants import INPUT_CHANNEL_RANGE, MAX_INPUT_CHANNEL_COUNT_PER_REMOTE, AUX_CHANNEL_RANGE


def write_remote_setup_xml(input_params, aux_params):
	ch_index_in_remote = 0

	ctrl_lists = []
	entry_lists = []

	ctrl_list = ''
	entry_list = ''

	# channel_id: globally unique id through all type of channels (input, aux, etc.)
	for channel_id in INPUT_CHANNEL_RANGE:
		# local_channel_id: used in the name of the channel, only unique in one type of channels
		local_channel_id = channel_id - INPUT_CHANNEL_RANGE.start

		if ch_index_in_remote == MAX_INPUT_CHANNEL_COUNT_PER_REMOTE:
			ch_index_in_remote = 0
			ctrl_lists.append(ctrl_list)
			ctrl_list = ''
			entry_lists.append(entry_list)
			entry_list = ''

		for param in input_params:
			# For debugging
			if param.scale == '':
				continue

			nrpn = int(param.nrpn) + channel_id * 128
			ctrl_list += f'\n<ctrl><name>IN{local_channel_id + 1} {param.param_name}</name><stat>2</stat><chan>0</chan>'
			ctrl_list += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
			entry_list += f'\n<entry ctrl="IN{local_channel_id + 1} {param.param_name}">'
			entry_list += f'\n<value><device>VST Mixer</device><chan>{channel_id}</chan>'
			entry_list += f'<name>{param.control}</name><flags>0</flags></value>'
			entry_list += f'\n</entry>'
		ch_index_in_remote += 1

	# The AUX, DCA and MAIN channels can go in the last remote.
	# They fit now, but if the channel counts change it might not.
	# An exception is thrown when it overflows, but it has to be fixed manually.
	# TODO
	for channel_id in AUX_CHANNEL_RANGE:
		local_channel_id = channel_id - AUX_CHANNEL_RANGE.start

		for param in aux_params:
			nrpn = int(param.nrpn) + channel_id * 128
			ctrl_list += f'\n<ctrl><name>AUX{local_channel_id + 1} {param.param_name}</name><stat>2</stat><chan>0</chan>'
			ctrl_list += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
			entry_list += f'\n<entry ctrl="AUX{local_channel_id + 1} {param.param_name}">'
			entry_list += f'\n<value><device>VST Mixer</device><chan>{channel_id}</chan>'
			entry_list += f'<name>{param.control}</name><flags>0</flags></value>'
			entry_list += f'\n</entry>'

	ctrl_lists.append(ctrl_list)
	entry_lists.append(entry_list)

	# Put everything in generic remote description files
	for i in range(len(ctrl_lists)):
		remote_setup_str = f'<?xml version="1.0" encoding="UTF-8"?>'
		remote_setup_str += f'\n<remotedescription version="1.1">'
		remote_setup_str += f'\n<ctrltable name="Standard MIDI">{ctrl_lists[i]}'
		remote_setup_str += f'\n</ctrltable>'
		remote_setup_str += f'\n<bank name="VST">{entry_lists[i]}'
		remote_setup_str += f'\n</bank>'
		remote_setup_str += f'\n</remotedescription>\n'

		remote_setup_xml = open(f'D:\\IT Projects\\Idea\\midimapper\\resources\\remote_setup{i}.xml', 'w')
		remote_setup_xml.write(remote_setup_str)
		remote_setup_xml.close()
