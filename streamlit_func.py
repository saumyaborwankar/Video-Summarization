import os
import streamlit as st
import io

import librosa

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip, concatenate_videoclips


def VideoToAudio(path):
    cmd='ffmpeg -y -i {} {}.wav'.format(path,'output/sample')
    os.system(cmd)
    
def ShowVideo(path):
    video_file = open(path, 'rb')
    video_bytes = video_file.read()
    st.video(video_bytes)

def ShowAudio(path):
    audio_file = io.open(path, 'rb')
    audio_bytes = audio_file.read()
    st.markdown('<h3>Here is the audio file </h3>',unsafe_allow_html=True )

def clear_file(path):
    for root, dirs, files in os.walk('./'+path):
        for f in files:
            os.unlink(os.path.join(root, f))
        for d in dirs:
            shutil.rmtree(os.path.join(root, d))

def Generate_summary():
    video_path='data/videos/sample.mp4'
    audio_path='output/sample.wav'
    x,sr=librosa.load(audio_path,sr=16000)
    print("The length of the audio clip is {} minutes".format(librosa.get_duration(x,sr)/60))
    split=5
    window_length=split*sr
    energy = np.array([sum(abs(x[i:i+window_length]**2)) for i in range(0, len(x), window_length)])
    df=pd.DataFrame(columns=['energy','start','end'])
    thresh=12000
    row_index=0
    for i in range(len(energy)):
        value=energy[i]
        if(value>=thresh):
            i=np.where(energy == value)[0]
            df.loc[row_index,'energy']=value
            df.loc[row_index,'start']=i[0] * 5
            df.loc[row_index,'end']=(i[0]+1) * 5
            row_index= row_index + 1
    temp=[]
    i=0
    j=0
    n=len(df) - 2
    m=len(df) - 1
    while(i<=n):
        j=i+1
        while(j<=m):
            if(df['end'][i] == df['start'][j]):
                df.loc[i,'end'] = df.loc[j,'end']
                temp.append(j)
                j=j+1
            else:
                i=j
                break
    df.drop(temp,axis=0,inplace=True)
    start=np.array(df['start'])
    end=np.array(df['end'])
    for i in range(len(df)):
        if(i!=0):
            start_lim = start[i] - 5
        else:
            start_lim = start[i] 
        end_lim   = end[i]   
        filename= "output/temp/"+ str(i+1) + ".mp4"
        ffmpeg_extract_subclip(video_path,start_lim,end_lim,targetname=filename)
    video=[]
    j=0
    a=[]
    for file in os.listdir('output/temp'):
        if file.endswith(".mp4"):
            a.append(int(file.split(".")[0])
            for files in sorted(a):
                print(files)
                video_temp=VideoFileClip(os.path.join(dir,"{}.mp4".format(files)))
                video.append(video_temp)
    print(len(video))
    print("----------------------------------------------")
    final_video= concatenate_videoclips(video)
    final_video.write_videofile("output/video/final_video.mp4")
    clear_file("output/temp/")