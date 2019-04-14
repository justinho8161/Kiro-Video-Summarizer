from dbSQL import *
from editing import *
import pickle
import os

pd.set_option('display.max_rows', 500)
infile = open('session.pkl','rb')
new_dict = pickle.load(infile)
infile.close()

link = 'https://www.youtube.com/watch?v=iCvmsMzlF7o&pbj'
model = Editor(link, bucket_name='hos123', run = True)

outfile = open('session.pkl','wb')
pickle.dump(model, outfile)
outfile.close()

infile = open('session.pkl','rb')
new_dict = pickle.load(infile)
infile.close()

new_dict.df[new_dict.df.Duration <3].mean()
new = Database(new_dict, run=False)
new_dict.title
new.find_entry(new_dict.title)


os.chdir('/home/justin/Downloads/Capstone/static/videos')
new_test.summarized_video(new_test.combine_sentences())


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
