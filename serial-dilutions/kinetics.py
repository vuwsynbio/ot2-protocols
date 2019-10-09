from opentrons import labware, instruments, robot
import logging
logging.basicConfig(level=logging.DEBUG)

metadata = {
	'protocolName':'NAD kinetics assay',
	'author':'Alex Telfar <te1farac@gmail.com>',
	'source':'kinetics.py'
}

def load_labware():
    wells96 = labware.load('corning_96_wellplate_360ul_flat', '1')
    liquid_input = labware.load('opentrons_10_tuberack_nest_4x50ml_6x15ml_conical', '2')
    tiprack300 = labware.load('tiprack-200ul', '3')

    pipette300 = instruments.P300_Single(
        mount='left',
        tip_racks=[tiprack300])

    # pipette10 = instruments.P10_Single(
    #     mount='right',
    #     tip_racks=[tiprack10])

    return (pipette300,
            # pipette10,
            liquid_input['A3'],  # trash
            liquid_input['A4'],  # buffer source,
            liquid_input['A1'],  # nad source
            liquid_input['A2'],  # enzyme source
            liquid_input['B1'],  # substrate source
            wells96)  # 96 well plate

def serial_dilution(pipette, substrate_source, dilutant_source, output, trash,
    total_mixing_volume, num_of_dilutions, dilution_factor):
    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    # Distribute diluent across the plate to the the number of samples
    # And add diluent to one column after the number of samples for a blank
    for col in output.cols(*range(2, num_of_dilutions+1)):
        pipette.distribute(total_mixing_volume, dilutant_source, col)

    for row in output.rows():
        pipette.transfer(
            transfer_volume,
            row.wells(*range(1, num_of_dilutions)),
            row.wells(*range(2, num_of_dilutions+1)),
            mix_after=(3, total_mixing_volume / 2))

        pipette.transfer(
            transfer_volume,
            row.wells(num_of_dilutions),
            trash)


def run_custom_protocol(
        dilution_factor: float=2.0,
        num_of_dilutions: int=4,
        replicates: int=6,
        total_mixing_volume: float=200.0,
        substrate_conc: float=1,  # 1M conc
        nad_conc: float=20.0,  # 10mM of NAD
        v_enzyme: float=50.0, # 5uL of enzyme
        ):

    transfer_volume = total_mixing_volume/dilution_factor
    diluent_volume = total_mixing_volume - transfer_volume

    p300, trash, buffer_s, nad_s, enzyme_s, substrate_s, wells96 = load_labware()

    # serial dilution of the substrate
    serial_dilution(p300, substrate_s, buffer_s, wells96, trash, 100, 4, 0.5)

    # add 10mM of NAD to each well
    p300.distribute(nad_conc, nad_s, wells96.wells())

    # add 5uL of enzyme to each well
    p300.distribute(v_enzyme, enzyme_s, wells96.wells())


if __name__ == '__main__' or __name__ == 'builtins':
	run_custom_protocol()
