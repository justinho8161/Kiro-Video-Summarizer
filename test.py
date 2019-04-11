import sqlite3
conn = sqlite3.connect('example.db')



link = 'https://www.youtube.com/watch?v=chVOJ7AzIMg'
model = Editor(link, bucket_name='hos123', run = True)

pd.set_option('display.max_rows', 500)
test = model.df
model.df.to_csv
test = test[test['Duration']>2].reset_index()


test1 = test['index'].values
test1

for i,j in enumerate(test['index'].values):
    previousIndex = j-1
    beginTC = test[test['index'] == j]['TimeIn'].values
    endTC = test[test['index'] == j]['TimeOut'].values
    if test['index'].values[i-1] == previousIndex:
        print(endTC)
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
