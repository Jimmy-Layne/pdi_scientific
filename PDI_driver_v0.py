# PDI specific Libraries
import lib.timeSeries as ts
import lib.utilities as ut
import lib.eld_computation as eld
import lib.met_computation as met
import lib.visualizations as vis
# General python libraries
import argparse as arg
import numpy as np


'''This script is designed as the v0 driver for the PDI testing program. '''

parser=arg.ArgumentParser()

parser.add_argument('fileNames',metavar='fN',type=str,nargs='+',help='The name of a file, or directory to be analyzed by the DVTvis Function')
parser.add_argument('channel',metavar='cH',type=str,nargs='+',help="This is the name of the channel to be analyzed, it should be formatted like 'DVT_CH1'")
args=parser.parse_args()

# This is the location of the config file, this used to be set by argparse, but users are not to be trusted
config = "/home/mrmisanthropy/Projects/cirpas/Code/DVTparam.cfg"
# Separate out the arguments from the cli
dataPath = args.fileNames[0]
channel = args.channel[0]



# Load event file
events, tLims = ut.get_event_file(dataPath, channel)

# Set the rest of the parameters before initialization

dLims=(2.,max(events['size'])+5.)
dBins = 128

params=ut.get_config(config)
sFreq = params['sfreq']
# Initialize timeseries object
flight = ts.TimeSeries(events['arrival time'], events['size'],tLims,dLims,sFreq,dBins)


# Now initialize computation of ELD
eld_coeff = eld.effective_laser_diameter(events,flight.size_param)


import pdb
pdb.set_trace()

#Now initialize the computation of meteorological variables
# TODO: Figure out how you're passing Alen around, this is some bush league shit
lwc,conc,vol = met.met_comp(flight,eld_coeff,events['velocity'],params)


# Now run the visualization routines to check our work
atime=flight.rep_atime
# Time Series Plots
relative_time_counts = flight.time_counts/flight.time_param['delta']
vis.arrival_time_series(relative_time_counts,atime)
vis.pcntl_plot(flight.percentile,atime)
# Met Variable Plots
vis.vol_vis(flight.rep_diameter,vol)
vis.conc_vis(atime,conc)
vis.lwc_vis(atime,lwc)