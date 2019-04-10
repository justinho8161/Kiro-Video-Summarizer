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
import pygame
import os


# new_link
# video = VideoFileClip('test0403.mp4')
# video.show(t=5, interactive = True)




# def summarized_video(new_df, video_name, output_name):
#     video = VideoFileClip(video_name)
#     cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_df.TimeCodes.values]
#     concat_clips = concatenate_videoclips(cuts)
#     # .write_videofile(output_name + ' Summarized.mp4', codec = 'mpeg4')
#     return concat_clips
#
# concat_clips = summarized_video(new_link,'vw2SaHkGfss.mp4',"")
#
# k = [frame[:,:,0] for frame in concat_clips.iter_frames()]
# print(k.shape)
#
# type(concat_clips)
# link = 'https://www.youtube.com/watch?v=nGeKSiCQkPw'
# new_link, title, video_title = main(link)
# new_link
# title
# video_title

class Editor:
    def __init__(self, video_link, bucket_name):
        self.video_link = video_link
        self.bucket_name = bucket_name
        self.title = None
        self.video_title = None
        self.new_model = None
        self.transcript, self.summary, self.tfidf_per_word, self.df = None, None, None, None


    def start_yt_job(self):
        os.chdir('/home/justin/Downloads/Capstone/static/videos')
        ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format':'mp4'}
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

    def summarized_video(self):
        os.chdir('/home/justin/Downloads/Capstone/static/videos')
        video = VideoFileClip(self.title)
        cuts = [video.subclip(float(i),float(j)) for i,j in zip(self.df.TimeIn.values, self.df.TimeOut.values)]
        concatenate_videoclips(cuts).write_videofile(self.title, codec = 'mpeg4')
        concatenate_videoclips(cuts).save_frame(self.title[0:-4]+'.jpeg', t=1.5)

    # def run(self):
    #
    #     status = output_job(self.title, output_name=self.title[:-4], bucket_name = 'hos123')
    #     self.new_model = cleaning_modeling(status)
    #     summarized_video(self.new_model.df,title,title)
    #
    #     os.chdir('/home/justin/Downloads/Capstone/')
    #     return self.new_model, self.title, self.video_title




#
# def main(self, bucket_name = 'hos123'):
#     os.chdir('/home/justin/Downloads/Capstone/static/videos')
#     ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format':'mp4'}
#     with YoutubeDL(ydl_opts) as ydl:
#         info = ydl.extract_info(self.video_link, download=True)
#         title = ydl.prepare_filename(info)
#         video_title = info.get('title', None)
#
#     status = output_job(title, output_name=title[:-4], bucket_name = 'hos123')
#     new_model = cleaning_modeling(status)
#     summarized_video(new_model.df,title,title)
#
#     os.chdir('/home/justin/Downloads/Capstone/')
#     return new_model, title, video_title
#
#
# def output_job(video_name, output_name, bucket_name = 'hos123'):
#     video = VideoFileClip(video_name)
#
#     audio_clip = "{}.mp3".format(video_name[:-4])
#     video.audio.write_audiofile(audio_clip, fps = 44100)
#
#
#     transcription = TranscriptionJob(audio_clip)
#     transcription.upload_audio_s3(bucket_name = bucket_name)
#
#     job_uri = "https://s3.amazonaws.com/{}/{}".format(bucket_name,audio_clip)
#     status = transcription.transcribe_job(output_name, job_uri, 'mp3')
#     return status
#
# def cleaning_modeling(status):
#     new_transcript = TranscriptCleaning(status)
#     new_model = Model_Analysis(new_transcript)
#     new_model.fit_TFIDF()
#     new_model.construct_df()
#     # df = pd.DataFrame(data, columns = ['TimeCodes','Sentence','Cleaned_Sentence', 'TFIDF'])
#     # new_df = df[(df['TFIDF']>df['TFIDF'].mean()) & ((df['Cleaned_Sentence'].str.count(' ')+1)>3)]
#     return new_model
#
# def summarized_video(new_df, video_name, output_name):
#     video = VideoFileClip(video_name)
#
#     cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_df.TimeCodes.values]
#     concatenate_videoclips(cuts).write_videofile(output_name, codec = 'mpeg4')
#
#     concatenate_videoclips(cuts).save_frame(output_name[0:-4]+'.jpeg', t=1.5)


#One big problem was that tf idf of the whole speech didn't work at all because stories were linear. All speeches have a linear progression leading up to the conclusion, so we had to figure out a way to
