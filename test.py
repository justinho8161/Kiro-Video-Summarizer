from editing import *
from moviepy.editor import *
from moviepy.video.compositing import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *

link = 'https://www.youtube.com/watch?v=QXBDOSJPGbo'
model = Editor(link, bucket_name='hos123')


model.start_yt_job()
status = model.output_job()
model.cleaning_modeling(status)
test = model.df
test




os.chdir('/home/justin/Downloads/Capstone/static/videos')
video = VideoFileClip(model.title)
cuts = [video.subclip(float(i),float(j)) for i,j in zip(test.TimeIn.values, test.TimeOut.values)]

# cuts = [video.subclip(float(i[0]),float(i[1])) for i in model.df.TimeCodes.values]
concatenate_videoclips(cuts).write_videofile(model.title[0:-4]+'s.mp4', codec = 'mpeg4')
concatenate_videoclips(cuts).save_frame(model.title[0:-4]+'s.jpeg', t=1.5)



model.summarized_video()
