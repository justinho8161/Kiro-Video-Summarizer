from dbSQL import *
from editing import *
import pickle
import os

# outfile = open('session.pkl','wb')
# pickle.dump(model, outfile)
# outfile.close()
pd.set_option('display.max_rows', 500)
infile = open('session.pkl','rb')
new_dict = pickle.load(infile)
infile.close()

os.chdir('/home/justin/Downloads/Capstone/static/videos')
new_test.summarized_video(new_test.combine_sentences())


def summarized_video():
    video = VideoFileClip(new_dict.title)
    cuts = [video.subclip(float(i),float(j)) for i,j in zip(new_dict.df.TimeIn.values,new_dict.df.TimeOut.values)]
    concatenate_videoclips(cuts).write_videofile(new_dict.title[0:-4]+'s.mp4', codec = 'mpeg4')
    os.chdir('/home/justin/Downloads/Capstone')
summarized_video()
combine_sentences(test)

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
