from moviepy.editor import *
from moviepy.video.compositing import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *
from transcript_cleaning import *
from model import *
from transcription_job import *
import pandas as pd
from __future__ import unicode_literals
import youtube_dl
from youtube_dl import YoutubeDL
import pygame


link = 'https://www.youtube.com/watch?v=3BRLGRqj8ps'
new_link = main(link)
new_link
video = VideoFileClip('test0403.mp4')
video.show(t=5, interactive = True)




def summarized_video(new_df, video_name, output_name):
    video = VideoFileClip(video_name)
    cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_df.TimeCodes.values]
    concat_clips = concatenate_videoclips(cuts)
    # .write_videofile(output_name + ' Summarized.mp4', codec = 'mpeg4')
    return concat_clips

concat_clips = summarized_video(new_link,'vw2SaHkGfss.mp4',"")

k = [frame[:,:,0] for frame in concat_clips.iter_frames()]
print(k.shape)

type(concat_clips)

def main(video, bucket_name = 'hos123'):
    ydl_opts = {'outtmpl': '%(id)s.%(ext)s', 'format':'mp4'}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video, download=True)
        title = ydl.prepare_filename(info)
        video_title = info.get('title', None)

    status = output_job(title, output_name=title[:-4], bucket_name = 'hos123')
    df = cleaning_modeling(status)
    summarized_video(df,title,video_title)
    return df


def output_job(video_name, output_name, bucket_name = 'hos123'):
    video = VideoFileClip(video_name)

    audio_clip = "{}.mp3".format(video_name[:-4])
    video.audio.write_audiofile(audio_clip, fps = 44100)

    transcription = TranscriptionJob(audio_clip)
    transcription.upload_audio_s3(bucket_name = bucket_name)

    job_uri = "https://s3.amazonaws.com/{}/{}".format(bucket_name,audio_clip)
    status = transcription.transcribe_job(output_name, job_uri, 'mp3')
    return status

def cleaning_modeling(status):
    new_transcript = TranscriptCleaning(status)
    new_model = Model_Analysis(new_transcript)
    data = new_model.fit_TFIDF()
    df = pd.DataFrame(data, columns = ['TimeCodes','Sentence','Cleaned_Sentence', 'TFIDF'])
    new_df = df[(df['TFIDF']>df['TFIDF'].mean()) & ((df['Cleaned_Sentence'].str.count(' ')+1)>3)]
    return new_df

def summarized_video(new_df, video_name, output_name):
    video = VideoFileClip(video_name)
    cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_df.TimeCodes.values]
    concatenate_videoclips(cuts).write_videofile(output_name + ' Summarized.mp4', codec = 'mpeg4')


#One big problem was that tf idf of the whole speech didn't work at all because stories were linear. All speeches have a linear progression leading up to the conclusion, so we had to figure out a way to
