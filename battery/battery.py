from opentrons import labware, instruments, robot
import logging
logging.basicConfig(level=logging.DEBUG)

metadata = {
	'protocolName':'Battery Test Block',
	'author':'vuwsynbio igem Team <dave@seyb.com>',
	'source':'The exciting mind of David Seyb'
}

robot.reset()

tiprack = labware.load('opentrons_96_tiprack_300ul', '11')
STOCK = labware.load('opentrons_15_tuberack_falcon_15ml_conical', '9')
BATTERY = labware.load('corning_96_wellplate_360ul_flat', '8')
CONTROL = labware.load('corning_96_wellplate_360ul_flat', '5')
TEMPO = labware.load('corning_96_wellplate_360ul_flat', '6')

EVEN_WELLS = 2
ODD_WELLS = 1

# define some solutions #

cuso4_STOCK = STOCK['A1']
citric_STOCK = STOCK['A2']
glycrol_STOCK = STOCK['B1']
mq_STOCK = STOCK['B2']
tempo_STOCK = STOCK['C1']
enzyme_STOCK = STOCK['C2']

# define transfer amounts #

#all
cuso4_volume = 100

#Battery
citric_volume = 50
glycrol_volume = 100

tempo_volume = 100
enzyme_volume = 30


# Control +
mq_control_volume = 130

#Tempo +
mq_tempo_volume = 30


mix_times = 3
mix_volume = 200

def run_custom_protocol(	
	pipette_type: 'StringSe	lection...'='p300-Single',
	tip_use_strategy: 'StringSelection...'='use one tip'
	):
	logging.info("running custom protocol ...")
	if pipette_type == 'p300-Single':
		p300 = instruments.P300_Single(
            mount='right',
            tip_racks=[tiprack])
	else:
		raise ValueError('wrong pipette')

# function will distribute in even or odd wells start at 2 for cathode wells and 1 anode

	def doEveryOtherWell(use_stock, do_plate = BATTERY, dispence_volume = 300, do = ODD_WELLS, include_rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'], mix = False):
		p300.pick_up_tip()
		p300vol = 0
		p300maxVol = p300.max_volume
		for row in include_rows:
			for index in range(do,13,2):
				if p300vol <= 0.0:
					fills = ( p300maxVol - ( p300maxVol % dispence_volume ) ) / dispence_volume
					p300.aspirate(fills * dispence_volume, use_stock)
					p300vol = fills * dispence_volume
				well = row + str(index)
				p300.dispense(dispence_volume, do_plate[well])
				p300vol = p300vol - dispence_volume
		if(mix):
			for row in include_rows:
				for index in range(do,13,2):
					well = row + str(index)
					p300.mix(mix_times,mix_volume,do_plate[well])
		p300.drop_tip()

	def doSetup( plate = BATTERY):
		#Transfer 1 Add 100μL CuSO4 to all EVEN wells	
		doEveryOtherWell( use_stock=cuso4_STOCK, do_plate=plate, dispence_volume=cuso4_volume, do=EVEN_WELLS)
		#Transfer 2 Add 50μL citric acid to all ODD wells
		doEveryOtherWell( use_stock=citric_STOCK, do_plate=plate, dispence_volume=citric_volume, do=ODD_WELLS)
		#Add 100μL Glycerol to ODD wells
		doEveryOtherWell( use_stock=glycrol_STOCK, do_plate=plate, dispence_volume=glycrol_volume, do=ODD_WELLS)

	doSetup(BATTERY)
	doSetup(CONTROL)
	doSetup(TEMPO)

	# Transfer 4 and Mix Control Plate
	#Add 130μL MQ to ODD well on the control, mix after each addition
	doEveryOtherWell(mq_STOCK, CONTROL, mq_control_volume, do=ODD_WELLS, mix=True)
	
	#Tempo only
	#Add 30μL MQ to ODD wells
	doEveryOtherWell(mq_STOCK,TEMPO, mq_tempo_volume, do=ODD_WELLS, mix=False)
	#Add 100μL TEMPO-NH2 to ODD wells, mix after each solution
	doEveryOtherWell(tempo_STOCK,TEMPO, tempo_volume, do=ODD_WELLS, mix=True)

	#Battery
	#Add 100μL TEMPO-NH2 to ODD wells, mix after each solution
	doEveryOtherWell(tempo_STOCK,BATTERY, tempo_volume, do=ODD_WELLS, mix=False)
	#Add 30μL  enzyme to ODD wells
	doEveryOtherWell(mq_STOCK,BATTERY, enzyme_volume, do=ODD_WELLS, mix=True)
	

	





run_custom_protocol()
