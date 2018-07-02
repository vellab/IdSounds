#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 29 20:43:07 2018

@author: bharath
"""

import glob
from td_utils import *
import IPython
import numpy as np
import pyaudio
import pandas as pd
import csv
import os
import scipy
import sounddevice as sd
import soundfile as sf

chosen_length=5

def padandcrop(wavfilename):
    _, data = wavfile.read(wavfilename)
    print("possible length of "+wavfilename+" is:"+str(float(data.shape[0])/44100.0))
    paddabletime=float(chosen_length+1)-float(data.shape[0])/44100.0
    if(paddabletime>=0.0):
        print("Need to pad "+wavfilename+" with "+str(paddabletime))
        duration = paddabletime
        audio_in_file = wavfilename
        print("Appending period in milliseconds:",duration*1000)
        audio_out_file = './audio_train_new/'+os.path.basename(wavfilename)
        silent_segment=AudioSegment.silent(duration=duration*1000)#duration in milliseconds
        song = AudioSegment.from_wav(audio_in_file)
        final_song =  song +silent_segment
        final_song.export(audio_out_file, format="wav")
        w = wave.open(audio_in_file, 'rb')
        print("Original parameters before appending:",w.getparams())
        w = wave.open(audio_out_file, 'rb')
        print("Parameters after appending:",w.getparams())
        song = AudioSegment.from_wav(audio_out_file)
        final_song = song[:chosen_length*1000]
        final_song.export(audio_out_file, format="wav")
        w = wave.open(audio_out_file, 'rb')
        print("Final parameters after editing:",w.getparams())
    else:
        audio_in_file = wavfilename
        audio_out_file = './audio_train_new/'+os.path.basename(wavfilename)
        song = AudioSegment.from_wav(audio_in_file)
        final_song =  song[:(chosen_length+1)*1000]
        final_song.export(audio_out_file, format="wav")
        w = wave.open(audio_out_file, 'rb')
        print("Parameters after cropping:",w.getparams())
        song = AudioSegment.from_wav(audio_out_file)
        final_song = song[:chosen_length*1000]
        final_song.export(audio_out_file, format="wav")
        w = wave.open(audio_out_file, 'rb')
        print("Final parameters after editing:",w.getparams())
        

i=0

wavfilenames=glob.glob('/Users/bharath/Documents/Studies/CompEng/Projects/identifysound/audio_train/*')
"""
for wavfilename in wavfilenames:
    padandcrop(wavfilename)
"""   
targetDf=pd.read_csv('train.csv')
print(targetDf.head())
print(targetDf['label'].unique())