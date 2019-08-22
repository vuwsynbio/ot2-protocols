from opentrons import labware, instruments, robot
import logging
logging.basicConfig(level=logging.DEBUG)

metadata = {
	'protocolName':'Battery Test Block',
	'author':'vuwsynbio igem Team <dave@seyb.com>',
	'source':'The exciting mind of David Seyb'
}

def run_custom_protocol(
	pipette_type: 'StringSelection...'='p300-Single',
	dilution_factor: float=2.0,
	num_of_dilutions: int=4,
	total_mixing_volume: float=200.0,
	tip_use_strategy: 'StringSelection...'='use one tip'):

	if pipette_type == 'p300-Single':
		pipette = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
	else:
		raise ValueError('wrong pipette')

# define some solutions #

	cuso4_stock = liquid_input['A1']
	citric_stock = liquid_input['A2']
	glycrol_stock = liquid_input['B1']
	mq_stock = liquid_input['B2']
	tempo_stock = liquid_input['C1']
	enzyme_stock = liquid_input['C2']

	cusof_volume = 100

# add cusof to all even numbered cells
	for index in range(2,12,2):
		for row in ['A', 'B']:
			well = row + str(index)
				logging.info(liquid_output[well])
			pipette.distribute(cusof_volume, cuso4_stock, liquid_output[well])
#
#	for col in liquid_output.cols('2', length=(num_of_dilutions)):
#		logging.info(col)
#		pipette.distribute(diluent_volume, cuso4_stock, col)
#		logging.info(col)
#		# col = col + 1

#	for row in liquid_output.rows():
#		pipette.transfer(
#			transfer_volume,
#			row.wells('1', to=(num_of_dilutions-1)),
#			row.wells('2', to=(num_of_dilutions)),
#			new_tip='once',
#			mix_after=(3, total_mixing_volume / 2))
#

# logging.info(__name__)
if __name__ == '__main__' or __name__ == 'builtins':
	robot.reset()

	# labware from https://labware.opentrons.com/

	tiprack = labware.load('opentrons_96_tiprack_300ul', '11')
	liquid_input = labware.load('opentrons_15_tuberack_falcon_15ml_conical', '9')
	liquid_output = labware.load('corning_96_wellplate_360ul_flat', '3')

	run_custom_protocol()
