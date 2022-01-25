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
