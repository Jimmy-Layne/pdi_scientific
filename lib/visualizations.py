import matplotlib.pyplot as plt
import numpy as np


'''This module holds all of the figure creation and matplotlib visualizations that we need.'''

def pcntl_plot(dsd_pcntl, arrival_time, save=False, show=True, sv_path=None):
    # Next plot a time series of percentiles
    fig = plt.figure()
    ax = fig.add_subplot(111)
    # DSD percentiles are organized like: [1,5,10,25,50,75,90,95,99]
    ax.plot(arrival_time, dsd_pcntl[:, 4], 'k', label="50th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 5], 'g', lw=0.75, label="75th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 3], 'g--', lw=0.75, label="25th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 6], 'r', lw=0.75, label="90th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 2], 'r--', lw=0.75, label="10th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 8], 'b', lw=0.75, label="99th Pcntl")
    ax.plot(arrival_time, dsd_pcntl[:, 0], 'b--', lw=0.75, label="1st Pcntl")

    plt.title("Time series of DSD percentiles percentile")
    plt.xlabel("Arrival time (s)")
    plt.ylabel(r"diameter ($\mu m$)")
    plt.legend(loc="upper right", ncol=4)
    if show:
        plt.show()
    if save:
        assert (sv_path is not None), "No save path provided"
        plt.savefig(sv_path)

    #plt.close()

def arrival_time_series(time_counts,arrival_time,save=False, show=True, sv_path=None):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(arrival_time,time_counts,'bo',lw=.5)
    plt.title("Event Time Series")
    plt.xlabel("Time of Arrival (s)")
    plt.ylabel("Counts")

    if show:
        plt.show()
    if save:
        assert (sv_path is not None), "No save path provided"
        plt.savefig(sv_path)


def met_visualization(lwc,vol,conc,arrival_time, save=False, show=True, sv_path=None):
    '''This function will compute visualizations for all of the meteorological variables
    these functions can also be called individually in the same Way.'''

    # View Volume
    vol_vis(arrival_time,vol,save,show,sv_path)
    # Conc
    conc_vis(arrival_time, conc, save, show, sv_path)
    # LWC
    lwc_vis(arrival_time, lwc, save, show, sv_path)


def conc_vis(arrival_time,conc, save=False, show=True, sv_path=None):
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.plot(arrival_time,conc,'ro',lw=0.5)
    plt.title("Drop Concentration Visualization")
    plt.xlabel("Arrival Time (s)")
    plt.ylabel(r"Drop Concentration ($cm^2$)")

    if show:
        plt.show()
    if save:
        assert (sv_path is not None), "No save path provided"
        plt.savefig(sv_path)


def lwc_vis(arrival_time,lwc, save=False, show=True, sv_path=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(arrival_time,lwc,'bo',lw=0.5)
    plt.title("Liquid Water Content Visualization")
    plt.xlabel("Arrival Time (s)")
    plt.ylabel("Liquid Water Content (g)")

    if show:
        plt.show()
    if save:
        assert (sv_path is not None), "No save path provided"
        plt.savefig(sv_path)



def vol_vis(rep_diam,vol, save=False, show=True, sv_path=None):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(rep_diam,vol,'go',lw=0.5)
    plt.title("View Volume Visualization")
    plt.xlabel("Representative Diameter ($\mu m$)")
    plt.ylabel(r"View Volume ($cm^3$)")
    sv_path=sv_path + ""
    if show:
        plt.show()
    if save:
        assert (sv_path is not None), "No save path provided"
        plt.savefig(sv_path)