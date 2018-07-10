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

# LOG_NAME = "/home/mrmisanthropy/Projects/pdi_scientific/pdi_logfile/pdiRun_{}_{}.log".format(channel, now.strftime("%Y-%m-%d_%H-%M"))
# fh = lg.FileHandler(LOG_NAME)
# fh.setLevel(lg.DEBUG)
# formatter = lg.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
# lg.addHandler(fh)


print("Initializing event file...")
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
eld_coeff, diam_fit = eld.effective_laser_diameter(events,flight.size_param)

#Now initialize the computation of meteorological variables
# TODO: Figure out how you're passing Alen around, this is some bush league shit
lwc,conc,vol,PVD = met.met_comp(flight,eld_coeff,events['velocity'],params)
print("Finished!")






##########################################
# Begin Client


stdscr = cs.initscr()
cs.echo()




while True:
    stdscr.erase()
    cs.flushinp()
    in_loc = mnu.home_screen(stdscr)
    stdscr.addstr(in_loc[1],in_loc[0],"Your Choice:")
    c = stdscr.getch()

    if c == ord('a'):
        vquit=False
        while not vquit:
            stdscr.erase()
            cs.flushinp()
            in_loc = mnu.vis_screen(stdscr)
            stdscr.addstr(in_loc[1], in_loc[0], "Your Choice:")
            vc = stdscr.getch()
            atime = flight.rep_atime
            figSave = params['svPath']
            if vc == ord('a'):
                relative_time_counts = flight.time_counts / flight.time_param['delta']
                vis.arrival_time_series(relative_time_counts, atime, show=True, sv_path=figSave, save=False)
            elif vc == ord('b'):
                vis.pcntl_plot(flight.percentile, atime, show=True, sv_path=figSave, save=False)
            elif vc == ord('c'):
                rep_vol = vol / flight.time_param['delta']
                vis.vol_vis(flight.rep_diameter, rep_vol, show=True, sv_path=figSave, save=False)
            elif vc == ord('d'):
                vis.conc_vis(atime, conc, show=True, sv_path=figSave, save=False)
            elif vc == ord('e'):
                vis.lwc_vis(atime, lwc, show=True, sv_path=figSave, save=False)
            elif vc == ord('f'):
                vis.pvd_vis(flight.rep_diameter, PVD, show=True, sv_path=figSave, save=False)
            elif vc == ord('q'):
                vquit = True
    elif c == ord('q'):
        break


    # elif ch == 2:
    #     print("Results from your Data File:")
    #     print("K0: {}".format(eld_coeff[0]))
    #     print("K1: {}".format(eld_coeff[1]))
    #     print("Total number of drops: {}".format(len(events)))
    #     print("For more detailed fitting results please see the log.")
    # elif ch==3:
    #     mnu.save_screen()
    # elif ch==4:
    #     quit =True
    # else:
    #     print("Err, that wasnt one of the menu options. Try again.")


