import numpy as np
from scipy.stats.mstats import gmean
import matplotlib.pyplot as plt
import lib.timeSeries as tseries
'''This module contains the meteorological quantities related to the data from the PDI.'''


def met_comp(ts,eld,vel_events,param):
    '''This function drives the computation of all of the other quantities. It expects an initialized
    timeseries object, and parameter dict with: ap_len, '''

    #density of water set at 1000g/cm^3
    rho_w=1000.00
    Nd = ts.size_param['num_bins']
    rep_diameter=ts.rep_diameter
    #Calculate the mass of water at each representative diameter
    w_mass=4./3.*np.pi*(rep_diameter*1.0e-4/2.0)**3 * rho_w*1e3
    # Now we need to compute the view-volume for each bin
    vol, PVD = view_volume(ts,vel_events,eld,param['aLen'])
    # These will hold our concentration and Liquid Water Content timeseries'
    conc_time_series = np.zeros((ts.time_param['num_bins']))
    lwc_time_series = np.zeros((ts.time_param['num_bins']))

    # Now we loop through each of the time bins, computing concentration and LWC based on that bins' DSD
    # after the computation we sum those series' and obtain our total conc and LWC for that bin.

    for i in range(ts.time_param['num_bins']):
        conc_series=concentration(vol,Nd,ts.size_counts[i,:])
        lwc_series=w_mass * conc_series

        conc_time_series[i]= sum(conc_series)
        lwc_time_series[i] = sum(lwc_series)

    return lwc_time_series,conc_time_series, vol, PVD


def view_volume(ts,vel_events,eld,ap_len):
    '''This function computes the view volume '''

    d=ts.rep_diameter
    # Currently the velocity is set to be the median of velocity events in (m/s)
    vm=np.median(vel_events)

    dt=ts.time_param['delta']
    # Q is now in m
    Q= vm*dt
    PVD = eld_model(eld,d)

    # Since the aperature length is provided, we can now compute the view volume for a
    # Given DSD
    # At present, Q is in meters, and D and l are in microns
    # We want the final volume to be in terms of cm^3 so we get:
    # 10^4(um)*10^-2(m)*10^4(um)=10^6
    tmpd = PVD * 1e-4
    tmpa = ap_len * 1e-4
    tmpq = Q * 1e2

    volume = tmpd * tmpa * tmpq

    return volume, PVD

def concentration(vol,nd,DSD):
    '''This function computes the concentration within one of the DSD bins
    using the view volume.'''
    conc=np.zeros((nd))
    for i in range(nd):
        if vol[i] < 1e-3:
            conc[i]=0.00
        else:
            tmp= DSD[i]/vol[i]
            conc[i] = tmp


    return conc


def eld_model(eld, d):
    D = np.zeros_like(d)
    E0=eld[0]
    E1=eld[1]
    # Because of the nature of our ELD equation, there is a lower limit on the size of the drops on which we can compute
    # view volume. First we need to determine the lowest allowable drop size based on the ELD as computed earlier.
    eld_floor = 10
        #np.exp(- E0 / E1)

    for i in range(len(d)):
        if d[i] == 0.0:
            D[i] = 0.0
        elif d[i] < eld_floor:
            try:
                D[i] = np.sqrt(E0 + E1 * np.log(eld_floor))
            except TypeError:
                import pdb
                pdb.set_trace()
        else:
            D[i] = np.sqrt(E0 + E1 * np.log(d[i]))

    return D
