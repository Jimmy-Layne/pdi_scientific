import pandas as pd
import numpy as np
import logging as lg
from os import path, listdir

'''This module holds the file loading and cleanup utillities for the PDI module'''
#This function combs through a directory for data files containing "DVT_data"
def get_files(_dir,flag):
    # Determine the files in the given directory
    _files=listdir(_dir)
    # Sort them, as chronology of filenames is important
    _files=np.sort(_files)
    # This is the identifier in the filename to search on
    data_list=[]
    for f in _files:
        if flag in f:
            data_out=path.join(_dir,f)
            data_list.append(data_out)
    return(data_list)

def get_config(cPath):
    ''' This function loads the config file and makes sure everything is correct'''

    params = {}
    with open(cPath, 'r') as f:
        for line in f:
            key,val = line.split(":")
            if key.rstrip() == "svPath":
                params[key.rstrip()] = val.rstrip()
            else:
                params[key.rstrip()] = float(val.rstrip())
    test_keys = ['sfreq','cmsk','aLen','stLimit','aqTime']
    for k in test_keys:
        if not k in params.keys():
            lg.warning("Warning, parameter {} not found in config file".format(k))
    return(params)


def set_time(f):
    # TODO: fix this weak filename time setting garbage, should invlove new parameter set in get_event_file call
    f=f.split("/")[-1]
    utc_time=f[14:22].split(" ")
    hour=float(utc_time[0])*3600.
    minute=float(utc_time[1])*60.
    start_time=hour+minute+float(utc_time[2])
    return(start_time)


def get_event_file(dataPath,channel):
    '''This is the main function for getting files from a data directory'''
    f_list=[]
    if(path.isfile(dataPath)):
        f_list.append(dataPath)

    elif(path.isdir(dataPath)):
        f_list.extend(get_files(dataPath,channel))

    else:
        print("Data Directory is not recognized, or maybe not created yet!")
    # File list is obtained, now we can create the single event file.
    events=pd.DataFrame()
    for f in f_list:
        tmp_ev=pd.read_csv(f)
        if tmp_ev.empty:
            continue
        else:
            tmp_ev.dropna(inplace=True)
            # Currently we have a lower limit set for drop sizes at 2 microns
            tmp_ev = tmp_ev[tmp_ev['size'] > 2.0]
        try:
            assert 'arrival time' in tmp_ev
            assert 'size' in tmp_ev
            assert 'velocity' in tmp_ev
            assert 'gate time' in tmp_ev
        except AssertionError:
            print("Improperly formatted headers in data file: {}".format(f))
            continue
        # Now we need to coordinate the time
        start_time=set_time(f)
        tmp_ev['arrival time']=tmp_ev['arrival time']+ start_time

        events=pd.concat([events,tmp_ev],ignore_index=True)
    tlims=(min(events['arrival time']),max(events['arrival time']))

    return events, tlims