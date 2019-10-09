from opentrons import labware, instruments
import logging
logging.basicConfig(level=logging.DEBUG)

metadata = {
	'protocolName':'Customizable Serial Dilution',
	'author':'Opentrons <protocol@opentrons.com>',
	'source':'Protocol Library'
}

liquid_input = labware.load('tube-rack-15_50ml', '2')
liquid_trash = liquid_input['A2']
liquid_output = labware.load('tube-rack-2ml', '1')
# couldnt load the  'tube-rack-1.5ml'
tiprack = labware.load('tiprack-200ul', '3')

def run_custom_protocol(
	pipette_type: 'StringSelection...'='p300-Single',
	dilution_factor: float=2.0,
	num_of_dilutions: int=4,
	total_mixing_volume: float=200.0,
	tip_use_strategy: 'StringSelection...'='use one tip'):

	pip_name = pipette_type.split('-')[1]

	if pipette_type == 'p300-Single':
		pipette = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
	else:
		raise ValueError('wrong pipette')

	transfer_volume = total_mixing_volume/dilution_factor
	diluent_volume = total_mixing_volume - transfer_volume

	logging.info(pipette)
	pipette.pick_up_tip()

	for col in []: #liquid_output.cols('2', length=(num_of_dilutions)):
		logging.info(col)

		pipette.distribute(diluent_volume, liquid_input['A1'], col)

	for row in liquid_output.rows():
		pipette.transfer(
			transfer_volume,
			row.wells('1', to=(num_of_dilutions-1)),
			row.wells('2', to=(num_of_dilutions)),
			mix_after=(3, total_mixing_volume / 2))

		pipette.transfer(
			transfer_volume,
			row.wells(num_of_dilutions),
			liquid_trash)

if __name__ == '__main__':
    run_custom_protocol()
