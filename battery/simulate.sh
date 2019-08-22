#!/usr/bin/env python
import opentrons.simulate
protocol_file = open('./battery.py')
runlog = opentrons.simulate.simulate(protocol_file)
print(opentrons.simulate.format_runlog(runlog))
