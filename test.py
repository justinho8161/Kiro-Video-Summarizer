from dbSQL import *
from editing import *
import pickle
import os
from cloud import wordCloud


# link = 'https://www.youtube.com/watch?v=iCvmsMzlF7o&pbj'
# model = Editor(link, bucket_name='hos123', run = True)
#
# outfile = open('session.pkl','wb')
# pickle.dump(model, outfile)
# outfile.close()


# https://www.google.com/search?client=ubuntu&channel=fs&q=https%3A%2F%2Fcodepen.io%2Fmineyazicioglu%2Fpen%2FaOYBay&ie=utf-8&oe=utf-8

os.chdir('/home/justin/Downloads/Capstone/static/videos')
# https://www.lifewire.com/srt-file-4135479

infile = open('session.pkl','rb')
new_dict = pickle.load(infile)
infile.close()


def create_transcript(model):
    new_index = model.df
    new_index['difference'] = pd.to_numeric(new_index['TimeOut'])-pd.to_numeric(new_index['TimeIn'])
    new_index['new_col'] = list(zip(new_index.Sentence, new_index.difference))

    file = open("{}.txt".format(model.title[:-4]),"w")
    count = 0
    for index,value in enumerate(new_index.new_col.values, start=1):
        file.write("c{} | {} | {} \n".format(index, value[0],count))
        count+=int(value[1])
    file.close()
    file = open("{}.txt".format(model.title[:-4]),"r")
    summarized_srt = []
    for line in file:
        line = line.strip().split("|")
        summarized_srt.append((line[0],line[2],line[1]))

    return summarized_srt


summarized_srt = create_transcript(new_dict)
summarized_srt


len(cue_time)
len(data_time)
len(transcript_lines)


file.write(“Hello World”)
file.write(“This is our new text file”)
file.write(“and this is another line.”)
file.write(“Why? Because we can.”)

file.close()


https://www.pythonforbeginners.com/files/reading-and-writing-files-in-python





words = len(new_dict.transcript.split(" "))
new_words = len(".".join(new_dict.df.Sentence.values).split(" "))
((words-new_words)/words)*100

new_dict.df[new_dict.df.Duration <3].mean()
new = Database(new_dict, run=True)

new.find_entry(new_dict.title)

new = Database(new_dict, run=True)
new.create_db()
new.close_db()


os.chdir('/home/justin/Downloads/Capstone/static/videos')
new_test.summarized_video(new_test.combine_sentences())
