import pandas as pd
import numpy as np
from scipy.stats.mstats import gmean
class TimeSeries:
    '''This is the class that contains the time series object for use in PDI analysis

    This object takes a 1d list and returns a histogram with counts, edges, and a reference list
    of the events in each bin.'''
    def __init__(self,time_events,size_events,tLimits,dLimits,sFreq, dbins):

        '''This is the constructor, it creates the edges for time and size series' then calls the creation functions'''
        #First compute the time series bin edges
        bins = int((tLimits[1] - tLimits[0])*sFreq)
        self.time_edges=np.linspace(tLimits[0],tLimits[1],bins)
        self.time_param={'min':tLimits[0],'max':tLimits[1],'type':"lin",'delta':self.time_edges[1]-self.time_edges[0],'freq':sFreq,'num_bins':bins}
        exponent=1./float(dbins)
        f=(dLimits[1]/dLimits[0])**exponent
        edges=[]
        for i in range(dbins+1):
            tmp=dLimits[0]*f**i
            edges.append(tmp)
        self.size_edges=np.asarray(edges)
        self.size_param={'min':dLimits[0],'max':dLimits[1],'type':"log",'freq':f,'num_bins':int(dbins)}

        # This is the representative diameter of each bin used in met calculations
        self.rep_diameter = np.zeros((self.size_param['num_bins']))
        self.rep_diameter[0]=gmean([self.size_edges[0],self.size_edges[1]])
        for i in range(1,self.size_param['num_bins']):
            self.rep_diameter[i] = gmean([self.size_edges[i], self.size_edges[i + 1]])

        # this is the representative arrival time at each bin for use in visualizations.
        self.rep_atime=np.zeros((self.time_param['num_bins']))
        self.rep_atime[0] = self.time_edges[0]
        for i in range(1,self.time_param['num_bins']):
            self.rep_atime[i]=np.average([self.time_edges[i], self.time_edges[i-1]])

        #Now call the method to generate the time series
        self.create_time_series(time_events)

        #Now call the method to generate the drop size distribution
        self.create_DSD(size_events)



    def create_time_series(self,events):
        '''This function creates the time series, which is a linearly spaced histogram

    This function expects a 1d array of times to be sorted into bins. It creates an array of counts for each bin,
    as well as a list containing arrays at each bin which hold the index of the sorted items.'''
        times=pd.Series(events)
        self.time_reference=[]
        for i in range(self.time_param['num_bins']):
            self.time_reference.append([])
        self.time_counts=np.zeros((self.time_param['num_bins']))

        #Now, loop through each element in the times array, and compute the bin hat it
        #Belongs in
        for event in times.items():
            cur_bin=int(self.find_bin(event[1],type='lin'))
            try:
                _list=self.time_reference[cur_bin]
                _count=self.time_counts[cur_bin]
            except IndexError:
                print("Invalid index returned in time series")
                continue
            self.time_reference[cur_bin].append(event[0])
            self.time_counts[cur_bin]=self.time_counts[cur_bin]+1

    def create_DSD(self,events):

        '''This function creates the drop-size-distribution (DSD) based on the time series that was already created

        This function expects a 1d array of diameter values. It takes the list of indexes in each time series bin and creates a
        log-spaced histogram of the associated diameter values. It also computes percentiles of the DSD at each bin.'''

        # This is a debugging object to ensure that counting is respected in DSD calculations
        tmp=np.arange(0,len(events))
        master_reference_list=pd.DataFrame(data=tmp,columns=['event_index'])
        master_reference_list['found']=False





        #This array holds all of the percentiles we wish to calculate on the distribution
        pcalc=[1,5,10,25,50,75,90,95,99]



        self.percentile=np.zeros((self.time_param['num_bins'],len(pcalc)))
        self.size_counts=np.zeros((self.time_param['num_bins'],self.size_param['num_bins']))
        it_check = 0
        for i in range(self.time_param['num_bins']):
            dlist=self.time_reference[i]
            if not dlist:
                continue

            # Here Is where the check is done against the master_reference
            for d in dlist:
                try:
                    line=master_reference_list.loc[d]
                except KeyError:
                    print("Key provided is outside scope of master_reference.")
                if line.found == False:
                    master_reference_list.at[d,'found'] = True
                    it_check = it_check +1

                elif line.found == True:
                    print("Duplicate Index Located!")


            diam = [events[j] for j in dlist]

            # try:
            #     diam=[events[j] for j in dlist]
            # except KeyError:
            #     import pdb
            #     pdb.set_trace()

            for d in diam:
                cur_bin=self.find_bin(d,'log')
                try:
                    _count=self.size_counts[i,cur_bin]
                except IndexError:

                    print("Invalid index returned in DSD computation")
                if not (d>= self.size_edges[cur_bin]) and (d < self.size_edges[cur_bin +1]):
                    print("Invalid Bin returned!!")


                self.size_counts[i,cur_bin] = self.size_counts[i,cur_bin] +1

            for j in range(len(pcalc)):
                self.percentile[i,j]=np.percentile(diam,pcalc[j])
            try:
                assert sum(self.size_counts[i,:]) == len(diam)
            except AssertionError:
                print("diameter reference mismatched with total counts in DSD for bin {}".format(i))
        # Here the final check is made for under counting of events
        missing = sum(~master_reference_list['found'])
        try:
            assert not missing == 0
        except AssertionError:
            print("Missing entries in master reference list")




    def find_bin(self,event,type):
        if type=='log':
            tmp=event/self.size_param['min']
            home_bin=int(np.log(tmp)/np.log(self.size_param['freq']))
            return(home_bin)

        elif type == 'lin':
            norm_event=event-self.time_param['min']
            home_bin,_=divmod(norm_event, self.time_param['delta'])
            return(home_bin)

        else:
            print("Unrecognized series type in findbin")
