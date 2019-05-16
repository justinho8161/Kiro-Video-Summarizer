from __future__ import unicode_literals
from moviepy.editor import *
from moviepy.video.compositing import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *
import pyfiles.transcript_cleaning
import pyfiles.model
import pyfiles.transcription_job
import pandas as pd
import youtube_dl
from youtube_dl import YoutubeDL
import numpy as np
import os
import pyfiles.cloud

class Editor:
    def __init__(self, video_link, path,  bucket_name, run=False):
        self.path = path
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
        wordCloud(self.df.Cleaned_Sentence.values, self.title, run=True)
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
        new_tcs = sorted([[np.amin(i),np.amax(i)] for i in b], key= lambda x:x[1])
        return new_tcs

    def summarized_video(self,new_tcs):
        video = VideoFileClip(self.title)
        cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_tcs]
        concatenate_videoclips(cuts).write_videofile(self.title[0:-4]+'s.mp4')
        os.chdir('../..')

    def create_srt(self):
        new_index = self.df
        new_index['difference'] = pd.to_numeric(new_index['TimeOut'])-pd.to_numeric(new_index['TimeIn'])
        new_index['new_col'] = list(zip(new_index.Sentence, new_index.difference))

        file = open("{}.txt".format(self.title[:-4]),"w")
        count = 0
        for index,value in enumerate(new_index.new_col.values, start=1):
            file.write("c{} | {} | {} \n".format(index, value[0],count))
            count+=int(value[1])
        file.close()
