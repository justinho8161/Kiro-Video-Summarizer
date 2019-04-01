from moviepy.editor import *
from moviepy.video.compositing import *
from moviepy.video.fx.all import *
from moviepy.audio.fx.all import *
import re
from transcript_cleaning import *
from model import *
import pandas as pd
import pymongo
from pymongo import MongoClient
from transcription_job import *

transcription = TranscriptionJob('full_vuln.mp3')
transcription.upload_audio_s3(bucket_name ='hos123')
status = transcription.transcribe_job("test5", "https://s3.amazonaws.com/hos123/full_vuln.mp3", 'mp3')

model = pd.read_json('asrOutput.json')
model = TranscriptCleaning(model)

model.fit_TFIDF()

model1 = Model_Analysis()
model.fit_TFIDF()

def fit_TFIDF(cleaned_sentences):
    vectorizer = TfidfVectorizer(stop_words = 'english')
    response = vectorizer.fit_transform(cleaned_sentences)

    tfidf = response.toarray().sum(axis=0)
    feature_names = vectorizer.get_feature_names()

    tfidf_per_word = {}
    for i, word in enumerate(feature_names):
        tfidf_per_word[word] = tfidf[i]

    tf_sentence = []
    for sentences in model.tc_and_clean:
        count = 0
        sentence_count = 0
        for words in sentences[1].split(" "):
            if words in tfidf_per_word:
                count+=1
                sentence_count += tfidf_per_word[words.lower()]

        tf_sentence.append([sentences,(sentence_count/(count+1))])

    return tf_sentence

_(cleaned_sentences)






new_script = [fitting_TFIDF(i)[0:15] for i in three_parts]

flat_list = [item for sublist in new_script for item in sublist]

new_trans = [i[0] for i in flat_list]
new_trans
import string
full_transcript
table = str.maketrans('', '', string.punctuation)
cleaned_transcript = [w[1].translate(table) for w in full_transcript]
cleaned_transcript

new_full = []

for i,j in enumerate(cleaned_transcript):
    new_full.append([full_transcript[i],j])

new_trans
new_cut = []
for i in new_trans:
    for j in new_full:
        if i == j[1]:
            new_cut.append((j[0][0]))





# def partition(seq, num):
#     avg = len(seq) / float(num)
#     out = []
#     last = 0.0
#
#     while last < len(seq):
#         out.append(seq[int(last):int(last + avg)])
#         last += avg
#
#     return out
#
# three_parts = chunkIt(tc_and_cleaned,3)
# three_parts[0]
#
# summary = []
# for i in comments:
#     for j in i:
#         summary.append(w.translate(table))
#




video = VideoFileClip("The power of vulnerability _ Brené Brown-iCvmsMzlF7o.mp4")
cuts = [video.subclip(float(i[0]),float(i[1])) for i in new_cut]
concatenate_videoclips(cuts).write_videofile('full_vuln0328.mp4', codec = 'mpeg4')


model.sentence_cleaning()
model.fitting_TFIDF()

model.transcript

model.transcript.to_csv('full_vuln.csv')
df = pd.read_csv('full_vuln.csv')



cuts = [video.subclip(float(i[0]),float(i[1])) for j, i in enumerate(new_) if j%5 ==0]
concatenate_videoclips(cuts).write_videofile('full_vuln.mp4', codec = 'mpeg4')


video.audio.write_audiofile('full_vuln.mp3', fps = 44100)
sequence = []
for i, j in cuts:
    sequence.append(audio_fadeout(video.subclip(i[0], j[0]),1))
sequence
# sequence.write_videofile('test.mp4')
concatenate_videoclips(sequence).write_videofile('vuln.mp4', codec = 'mpeg4')
concatenate_videoclips(sequence).audio.write_audiofile('vuln.mp3', fps = 44100)




#One big problem was that tf idf of the whole speech didn't work at all because stories were linear. All speeches have a linear progression leading up to the conclusion, so we had to figure out a way to
