from read_csv import read_channel_csv
from write_map_xml import write_map_xml
from write_remote_setup_xml import write_remote_setup_xml


def main():
	input_params = read_channel_csv('ch-input.csv')
	aux_params = read_channel_csv('ch-aux.csv')
	dca_params = read_channel_csv('ch-dca.csv')
	write_map_xml(input_params, aux_params, dca_params)
	write_remote_setup_xml(input_params, aux_params, dca_params)


if __name__ == '__main__':
	main()
