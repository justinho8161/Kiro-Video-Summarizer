from __future__ import unicode_literals
from moviepy.editor import *
from moviepy.video.compositing import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *
from transcript_cleaning import *
from model import *
from transcription_job import *
import pandas as pd
import youtube_dl
from youtube_dl import YoutubeDL
import numpy as np
# import pygame
import os


class Editor:
    def __init__(self, video_link, bucket_name, run=False):
        os.chdir('/home/justin/Downloads/Capstone/static/videos')
        self.video_link = video_link
        self.bucket_name = bucket_name
        self.title = None
        self.video_title = None
        self.new_model = None
        self.transcript, self.summary, self.tfidf_per_word, self.df = None, None, None, None
        if run:
            self.run()

    def run(self):
        self.start_yt_job()
        status = self.output_job()
        self.new_model = self.cleaning_modeling(status)
        new_tcs = self.combine_sentences()
        self.summarized_video(new_tcs)


    def start_yt_job(self):
        ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format':'mp4', 'writethumbnail': True}
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.video_link, download=True)
            self.title = ydl.prepare_filename(info)
            self.video_title = info.get('title', None)

    def output_job(self):
        video = VideoFileClip(self.title)

        audio_clip = "{}.mp3".format(self.title[:-4])
        video.audio.write_audiofile(audio_clip, fps = 44100)

        transcription = TranscriptionJob(audio_clip)
        transcription.upload_audio_s3(bucket_name = self.bucket_name)

        job_uri = "https://s3.amazonaws.com/{}/{}".format(self.bucket_name,audio_clip)
        status = transcription.transcribe_job(self.title[0:-4], job_uri, 'mp3')
        return status

    def cleaning_modeling(self,status):
        new_transcript = TranscriptCleaning(status)
        self.new_model = Model_Analysis(new_transcript)
        self.new_model.fit_TFIDF()
        self.new_model.construct_df()

        self.transcript = self.new_model.transcript
        self.summary = self.new_model.summary
        self.tfidf_per_word = self.new_model.tfidf_per_word
        self.df = self.new_model.df

    def combine_sentences(self):
        data = self.df.reset_index()
        similar =[value-index for index,value in enumerate(data['index'].values,0)]

        consec_tcs = dict((el,[]) for el in list(set(similar)))

        for i,j in zip(similar,zip(data['TimeIn'].values,data['TimeOut'].values)):
            consec_tcs[i].append(np.array(j).astype(float))

        b = [np.concatenate(v).ravel().tolist() for k,v in consec_tcs.items()]
        new_tcs = [[np.amin(i),np.amax(i)] for i in b]
        # if (np.amax(i)-np.amin(i)) >=2
        return new_tcs


    def summarized_video(self,new_tcs):
        video = VideoFileClip(self.title)
        cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_tcs]
        concatenate_videoclips(cuts).write_videofile(self.title[0:-4]+'s.mp4', codec = 'mpeg4')
        os.chdir('/home/justin/Downloads/Capstone')

#One big problem was that tf idf of the whole speech didn't work at all because stories were linear. All speeches have a linear progression leading up to the conclusion, so we had to figure out a way to
