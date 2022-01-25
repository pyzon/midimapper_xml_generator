from read_csv import read_input_csv
from write_map_xml import write_map_xml
from write_remote_setup_xml import write_remote_setup_xml


def main():
	input_params = read_input_csv()
	write_map_xml(input_params)
	write_remote_setup_xml(input_params)


if __name__ == '__main__':
	main()
