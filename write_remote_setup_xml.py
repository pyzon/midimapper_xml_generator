from channel_names import dca_channel_names, aux_channel_names, input_channel_names
from constants import INPUT_CHANNEL_RANGE, MAX_INPUT_CHANNEL_COUNT_PER_REMOTE, AUX_CHANNEL_RANGE, DCA_CHANNEL_RANGE, \
	INPUT_PARAM_COUNT, MAX_PARAM_COUNT_PER_REMOTE, TOTAL_CHANNEL_COUNT, MAIN_CHANNEL_RANGE


def write_remote_setup_xml(input_params, aux_params, dca_params):
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

			name = f'IN{local_channel_id + 1} {input_channel_names[local_channel_id]} {param.param_name}'
			nrpn = int(param.nrpn) + channel_id * 128
			ctrl_list += generate_ctrl_xml(name, nrpn)
			entry_list += generate_entry_xml(name, channel_id, param.control)
		ch_index_in_remote += 1

	# The AUX, DCA and MAIN channels can go in the last remote.
	# They fit now, but if the channel counts get too big it might not and we need a new remote.
	param_count = ch_index_in_remote * INPUT_PARAM_COUNT

	# AUX channels
	for channel_id in AUX_CHANNEL_RANGE:
		local_channel_id = channel_id - AUX_CHANNEL_RANGE.start
		for param in aux_params:
			nrpn = int(param.nrpn) + channel_id * 128
			name = f'AUX{local_channel_id + 1} {aux_channel_names[local_channel_id]} {param.param_name}'
			ctrl_list += generate_ctrl_xml(name, nrpn)
			entry_list += generate_entry_xml(name, channel_id, param.control)
			param_count += 1

	# DCA channels that are DCAs on the console as well
	for channel_id in DCA_CHANNEL_RANGE:
		local_channel_id = channel_id - DCA_CHANNEL_RANGE.start
		for param in dca_params:
			nrpn = int(param.nrpn) + channel_id * 128
			name = f'DCA{local_channel_id + 1} {dca_channel_names[local_channel_id]} {param.param_name}'
			ctrl_list += generate_ctrl_xml(name, nrpn)
			entry_list += generate_entry_xml(name, channel_id, param.control)
			param_count += 1

	# TODO DCA channels that are actually AUXes on the console

	# MASTER channel which is the last DCA
	for param in dca_params:
		nrpn = int(param.nrpn) + MAIN_CHANNEL_RANGE.start * 128
		name = f'MASTER {param.param_name}'
		channel_id = TOTAL_CHANNEL_COUNT
		ctrl_list += generate_ctrl_xml(name, nrpn)
		entry_list += generate_entry_xml(name, channel_id, param.control)
		param_count += 1

	if param_count > MAX_PARAM_COUNT_PER_REMOTE:
		raise OverflowError('The last remote is overflown. A new remote is needed.')

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


def generate_ctrl_xml(name, nrpn):
	ctrl = f'\n<ctrl><name>{name}</name><stat>2</stat><chan>0</chan>'
	ctrl += f'<addr>{nrpn}</addr><max>16383</max><flags>19</flags></ctrl>'
	return ctrl


def generate_entry_xml(name, channel_id, control):
	entry = f'\n<entry ctrl="{name}">'
	entry += f'\n<value><device>VST Mixer</device><chan>{channel_id}</chan>'
	entry += f'<name>{control}</name><flags>0</flags></value>'
	entry += f'\n</entry>'
	return entry
