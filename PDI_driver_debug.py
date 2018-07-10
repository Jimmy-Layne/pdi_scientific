# PDI specific Libraries
import lib.timeSeries as ts
import lib.utilities as ut
import lib.eld_computation as eld
import lib.met_computation as met
import lib.visualizations as vis
# General python libraries
import argparse as arg
import numpy as np


'''This script is designed as the  driver for testing the basic features of the PDI. '''

parser=arg.ArgumentParser()

parser.add_argument('fileNames',metavar='fN',type=str,nargs='+',help='The name of a file, or directory to be analyzed by the DVTvis Function')
parser.add_argument('channel',metavar='cH',type=str,nargs='+',help="This is the name of the channel to be analyzed, it should be formatted like 'DVT_CH1'")
args=parser.parse_args()

# This is the location of the config file, this used to be set by argparse, but users are not to be trusted
config = "/home/mrmisanthropy/Projects/pdi_scientific/pdi_config.cfg"
# Separate out the arguments from the cli
dataPath = args.fileNames[0]
channel = args.channel[0]



# Load event file
events, tLims = ut.get_event_file(dataPath, channel)

# Set the rest of the parameters before initialization
# Note, drops have been observed in VOCALS runs which are below 2 microns, the lower limit was then altered to 1.1
dLims=(1.1,max(events['size'])+5.)
dBins = 128

params=ut.get_config(config)
sFreq = params['sfreq']
# Initialize timeseries object
flight = ts.TimeSeries(events['arrival time'], events['size'], tLims, dLims,sFreq,dBins)


# Now initialize computation of ELD
eld_coeff,dFit = eld.effective_laser_diameter(events,flight.size_param)


#Now initialize the computation of meteorological variables
# TODO: Figure out how you're passing Alen around, this is some bush league shit
lwc,conc,vol,PVD = met.met_comp(flight,eld_coeff,events['velocity'],params)


# Now run the visualization routines to check our work
atime=flight.rep_atime
figSave=params['svPath']
# Time Series Plots
relative_time_counts = flight.time_counts/flight.time_param['delta']
# is.arrival_time_series(relative_time_counts,atime,show=True,sv_path=figSave,save=True)
# vis.pcntl_plot(flight.percentile,atime,show=True,sv_path=figSave,save=True)
# Met Variable Plots
# rep_vol = vol/flight.time_param['delta']
# vis.vol_vis(flight.rep_diameter,rep_vol,show=True,sv_path=figSave,save=True)
# vis.conc_vis(atime,conc,show=True,sv_path=figSave,save=True)
# vis.lwc_vis(atime,lwc,show=True,sv_path=figSave,save=True)