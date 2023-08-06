﻿# -*- coding: utf-8 -*-

###################################################################################
##Patricia Milz -- keypy library -- The KEY Institute for Brain-Mind Research    ##
##Please cite this repository and the paper where it was first applied when using##
##this library for your own research. Thank you!						         ##
###################################################################################

###################
#  Load packages  #
###################

import h5py
import numpy as np
import matplotlib.mlab as mlab
import os.path as op
import glob
from contextlib import closing


################################
#  Export from hdf5 to BESA    #
################################

'''
###########################
#  Info on BESA Format    #
###########################

NPTS=<number of data points> TSB=<point in time 0 in ms>
DI=<sampling interval in ms> SB=<scaling of data points in 1/�V>
SC=<display scaling (is ignored)> NCHAN=<number of channels>

The data values are entered as of the third line in the form of floating point numbers. The
decimal symbol used is always a decimal point. Each line contains the data of one channel.
The individual data values are separated by spaces.
If you store the data in a raw data folder, the Analyzer reads it in like a normal raw EEG.
'''

###    TO DO    ###
#Adapt to new database / classes model
#only use necessary parameters
#use useful default parameters in function
##--------------##

#input:
#inputhdf: input hdf5 file
#VP: list of VP names
#Cond: list of condition names
#outputfolder: folder that output will be written to
#TSB: point in time 0 in ms
#Fs: sampling frequency
#SB: scaling of data points in 1/�V
#SC: display scaling (is ignored)
#nch: number of channels
#database: name of hdf5 group of input processing stage (e.g. i_avgref)

def hdf5_to_besa(inputhdf, VP, Cond, outputfolder, TSB, Fs, SB, SC, nch, database):
    with closing( h5py.File(inputhdf, 'a') ) as f:
        for vpi in VP:
            print 'subject', vpi, '-------------------'
            for condi, cond in enumerate(Cond):
                if not vpi in f.keys():
                    continue
                if not cond in f['/%s' % vpi].keys():
                    continue

                group = f["/%s/%s" % (vpi, cond)]
                dset = group[database].value
               
                print 'processing', "/%s/%s" % (vpi, cond), 'shape', dset.shape
                
                #test if nch user matches nch file
                if nch != len(dset[0]):
                    print 'Channel number mismatch between inputhdf and manually specified number of channels'
                #number of timeframes in the whole file
                nodp=len(dset)
                #Line 1
                line1='NPTS=%d TSB=%d DI=%f SB=%d SC=%d NCHAN=%d' % (nodp, TSB, 1./Fs*1000, SB, SC, nch)
                #Line 2: channel names: Fp1 Fp2 F3 F4....
                #Line 3 space separated data points
                filename = '%s_%s' % (vpi, cond)
                with open( op.join( outputfolder, filename+'.txt'), 'w') as kk:
                    kk.writelines(line1)
                    kk.write('\n')
                    for ele in chlist:
                        kk.write('%s'%ele)
                        kk.write(' ')
                    kk.write('\n')
                    np.savetxt(fname=kk, X=dset.T, fmt=fmt, delimiter=' ')




################################
#  Export from hdf5 to ASCI    #
################################

'''
##############################
#  LORETA ASCI Requirements  #
##############################

rows = timeframes
columns = channels
'''

def hdf5_to_ascii(inputhdf5, database, eeg_info_study_obj, outputfolder, numberofepochs='all', fmt='%10.6f'):
    TF = eeg_info_study_obj.tf
    with closing( h5py.File(inputhdf5) ) as f:
        for groupi in f['/'].keys():
            for pti in f['/%s' % (groupi)].keys():
                for cond in f['/%s/%s' % (groupi, pti)].keys():
                    for run in f['/%s/%s/%s' % (groupi, pti, cond)].keys():
                        try:
                            timeframe_channel_dset = f['/{0}/{1}/{2}/{3}/{4}' .format(groupi, pti, cond, run, database)]
                        except:
                            print('not found',  ['/{0}/{1}/{2}/{3}/{4}' .format(groupi, pti, cond, run, database)])
                            continue
                    
                        path = '/{0}/{1}/{2}/{3}/{4}' .format(groupi, pti, cond, run, database)
                
                        print('writing to asci ', group, pti, cond, run)
                        timeframe_channel_dset = f[path]    
               
                        timeframe_channel=timeframe_channel_dset.value
                        dset = timeframe_channel

                        #Select only the first 'numberofepochs' 2 second epochs for export
                        if numberofepochs!='all':
                            if len(dset)>TF*numberofepochs:
                                dset = dset[0:TF*numberofepochs,:]
                            else:
                                print 'inputhdf: ', inputhdf, 'processing stage: ', database, 'did only contain: ', len(dset), 'timeframes. ', 'when a minimum of number of time frames per epoch times epoch length was expected: ', TF*numberofepochs 
                                    
                        filename = '%s_%s_%s_%s' % (groupi, pti, cond, run)
                        with open( op.join( outputfolder, filename+'.txt'), 'w') as kk:
                            np.savetxt(fname=kk, X=dset, fmt=fmt, delimiter=' ')

