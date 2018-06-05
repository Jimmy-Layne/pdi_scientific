# PDI specific Libraries
import lib.timeSeries as ts
import lib.utilities as ut
import lib.eld_computation as eld
import lib.met_computation as met
import lib.visualizations as vis
import lib.menu as mnu
# General python libraries
import argparse as arg
import curses as cs
import logging as lg

import datetime as dt
'''This program is designed to be a more robust interface for the PDI processing software.'''

###########################################################
# Begin Computation and analysis



# This is the config path provided to utilities, change as needed
config = "/home/mrmisanthropy/Projects/pdi_scientific/pdi_config.cfg"

# Initialize Argument Parser
parser=arg.ArgumentParser()
parser.add_argument('fileNames',metavar='fN',type=str,nargs='+',help='The name of a file, or directory to be analyzed by the DVTvis Function')
parser.add_argument('channel',metavar='cH',type=str,nargs='+',help="This is the name of the channel to be analyzed, it should be formatted like 'DVT_CH1'")
args=parser.parse_args()
# Extract arguments
dataPath = args.fileNames[0]
channel = args.channel[0]



# Initialize logger
now = dt.datetime.now()

LOG_NAME = "/home/mrmisanthropy/Projects/pdi_scientific/pdi_logfile/pdiRun_{}_{}.log".format(channel, now.strftime("%Y-%m-%d_%H-%M"))
fh = lg.FileHandler(LOG_NAME)
fh.setLevel(lg.DEBUG)
formatter = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# lg.addHandler(fh)


print("Initializing event file at {}".format(dataPath))
# Load full event file from individual pdi files
events, tLims = ut.get_event_file(dataPath, channel)
print("Success! total of {} events found".format(len(events)))
# Set the rest of the parameters before initialization
dLims=(2.0,max(events['size'])+5.)
dBins = 128

params=ut.get_config(config)
sFreq = params['sfreq']
print("Creating TimeSeries object.")
# Initialize timeseries object
flight = ts.TimeSeries(events['arrival time'], events['size'],tLims,dLims,sFreq,dBins)

print("Done!")
print("Computing Met Variables...")
# Now initialize computation of ELD
eld_coeff = eld.effective_laser_diameter(events,flight.size_param)

#Now initialize the computation of meteorological variables
# TODO: Figure out how you're passing Alen around, this is some bush league shit
lwc,conc,vol,PVD = met.met_comp(flight,eld_coeff,events['velocity'],params)
print("Run Success!")
