import numpy as np
import matplotlib.pyplot as plt
from scipy.stats.mstats import gmean
import lmfit as lm
import logging as lg

'''This Module contains the routines to compute quantities from pdi data

Effective laser diameter takes events(pandas dataframe) and param which should be the same as size_param
found in timeSeries.py. Currently fitting is done using lmfit, but this could potentially change in the
future. to fit the data, we compute a histogram of diameter, then for each bin, we create a local histogram of
the transit lengths, and fit the CDF of equation (4?)[cite] to that histogram. Using those parameters (D) and the geometric mean
of the diameter entries in each bin, we can fit equation 5 and determine the ELD coefficients for computation
of LWC, Conc, etc.'''


def effective_laser_diameter(events,param):
    '''This is the main function for computing ELD'''

    #Derived Quantities
    t_length=np.asarray(events['velocity']*events['gate time']*1e6)
    diam=np.asarray(events['size'])
    #Compute linear diameter histogram
    
    diam_edges=np.linspace(2.,max(diam)+10.,param['num_bins'])
    diam_list=[]
    diam_count=[]
    for i in range(1, len(diam_edges)):
        _Dlist = []
        _Dcount = 0
        _range = (diam_edges[i - 1], diam_edges[i])

        for t in range(len(diam[:])):
            temp = diam[t]
            if (_range[0] < temp <= _range[1]):
                _Dcount = _Dcount + 1
                _Dlist.append(t)
        diam_count.append(_Dcount)
        diam_list.append(_Dlist)
    
    diam_mask=[]    
    # Now compute diameter fitting over the bins who's count is at least 400
    # TODO: ELD stat limit needs to be placed into the config file
    for i in range(len(diam_count)):
        if (diam_count[i]>400):
            diam_mask.append(i)

    #Begin Fitting
    rep_diam=[]
    diam_fit=[]
    for m in diam_mask:
        local_list=diam_list[m]
        local_tlength=list(t_length[i] for i in local_list)
        rep_diam.append(gmean(list(diam[i] for i in local_list)))

        # Now we'll create a local histogram of transit lengths
        # Currently the bin width here is set to 10um
        len_width=10
        len_max=np.ceil(max(local_tlength))
        len_min=np.floor(min(local_tlength))
        len_bins=np.arange(len_min,len_max,len_width)
        len_list=[]
        len_count=[]
        
        for j in range(1, len(len_bins)):
            _list = []
            _count = 0
            for k in range(len(local_tlength[:])):
                temp = local_tlength[k]
                _range = (len_bins[j - 1], len_bins[j])
                if (_range[0] < temp <= _range[1]):
                    _count = _count + 1
                    _list.append(k)
            len_count.append(_count)
            len_list.append(_list)
        diam_fit.append(fit_length(len_count,len_list,local_tlength,len_bins))
    # Now we can fit to determine our ELD coefficients based on this file
    eld_coeff=diameter_fit(rep_diam,diam_fit)
    return(eld_coeff)

# Fitting routines
def fit_length(numEV, listEV, Tlength, Lbins,plot=False):

    '''This function fits the transit lengths in each diameter bin to our CDF. it returns the D parameter for that bin
     which can be associated with the representative diameter in that bin'''
    N = len(numEV)
    CDF = []
    #TODO: add fitting stats to put in these variables
    #Dval = []
    #Derr = []
    found = False
    tot = np.sum(numEV, dtype='float')
    # Now we'll compute discrete CDF values from the histogram
    for i in range(N):
        CDF.append(discrete_cdf(i, tot, numEV))
        # We need to determine where the CDF reaches 60% so that we can inform our
        # initial guess in the fit
        if (CDF[-1] > .6 and not found):
            iniGuess = i
            found = True

    # For the x data we'll use the midpoint of each bin
    Ldata = np.zeros_like(numEV)
    for i in range(1, len(Lbins)):
        #Would it be potentially better to use another geometric mean here? to be consistent with the ELD fit later?
        Ldata[i - 1] = (Lbins[i] - Lbins[i - 1]) / 2 + Lbins[i - 1]
    par = lm.Parameters()
    par.add('Diam', vary=True, value=Ldata[iniGuess])
    # Now we fit the descrete CDF values to the continuous CDF
    result = lm.minimize(continuous_cdf, par, args=(Ldata, CDF))
    fit = CDF + result.residual
    
    # these commands check answer with fit reports and plots
    # print(lm.fit_report(result))
    if plot:
        fig=plt.figure()
        ax=fig.add_subplot(111)
        plt.title("CDF plot")
        ax.plot(Ldata,CDF,'bo')
        ax.plot(Ldata,fit,'r')
        ax.set_ybound(lower=0.0,upper=2)
        plt.show()

    # now output the parameter values of each fit
    # we should also output some fitting statistics, but that can come later
    Dval = result.params.valuesdict()

    return Dval['Diam']

def diameter_fit(repDval, Dfit,plot=False):
    '''This function fits the D values output from the transit length fits, to the representative diameters computed 
    for each diameter bin by equation 5.'''
    N = len(Dfit)
    # First we'll need to generate the d values to be used
    Dfit = np.asarray(Dfit, dtype="float")
    repDval = np.asarray(repDval, dtype="float")
    params = lm.Parameters()
    params.add("K0", vary=True, value=1e-6)
    params.add("K1", vary=True, value=1e-8)
    result = lm.minimize(eld_model, params, args=(repDval, Dfit))
    #TODO: Write logging utillity
    print(lm.fit_report(result))
    
    if plot:
        # Plot check
        fit=Dfit+result.residual
        fig=plt.figure()
        ax=fig.add_subplot(111)
        plt.title("ELD fit")
        plt.plot(repDval,Dfit,'go',lw=.5)
        plt.plot(repDval,fit,"k--",lw=1)
        plt.show()

    Kvals = result.params.valuesdict()
    return ((Kvals['K0'], Kvals['K1']))

# Models
def discrete_cdf(ind, tot, numEV):
    '''This function computes a discrete cdf at the bin [ind] for some histogram passed to it'''
    cur = 0.0
    ind = ind + 1
    for n in range(ind):
        cur = cur + numEV[n]
    out = cur / tot
    return (out)

def continuous_cdf(par,l,y=None):
    '''This function holds our derived CDF function from equation (4?)
    We will be fitting the discrete cdf computed above to this function.'''
    D=par['Diam'].value
    x=l/D
    mod=np.zeros_like(x,dtype='float')
    for i in range(len(x)):
        if x[i]>=1:
            mod[i]=1
        else:
            mod[i]=(1-np.sqrt(1-(x[i])**2))
    if not y is None:
        return(mod-y)
    else:
        return mod

def eld_model(par,d,D=None):
    '''This function holds our model for equation 5'''
    K0=par['K0'].value
    K1=par['K1'].value

    mod=np.zeros_like(d,dtype="float")
    for i in range(len(d)):
        mod[i]=np.sqrt(K0+K1*np.log(d[i]))
    if not D is None:
        return(mod-D)
    else:
        return(mod)
