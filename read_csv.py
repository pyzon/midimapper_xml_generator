import csv
from Param import Param
from Point import Point


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
