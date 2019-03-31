import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from transcription_job import *
import string

class Model_Analysis:
    def __init__(self, status):
        self.status = status
        self.transcript = None
        self.tc_words = None

    def cleaning_transcript(self):
        new_link = self.status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        self.transcript = pd.read_json(new_link)
        real_transcript = self.transcript['results']['items']
        tc_and_words = []
        for i in real_transcript:
            if 'start_time' in i.keys():
                tc_and_words.append([i['start_time'],i['end_time'],i['alternatives'][0]['content']])
        self.tc_words = tc_and_words
        return self

    def sentence_cleaning(self):
        separated_sentences = self.transcript['results'][1][0]['transcript'].split(" ")
        sentences_period = self.transcript['results'][1][0]['transcript'].split(".")[0:-1]

        end_sentence = [i for i, word in enumerate(separated_sentences) if "." in word]

        tcs = []
        start = 0
        for i,j in enumerate(end_sentence):
            tcs.append([(self.tc_words[start][0],self.tc_words[j][-2]),sentences_period[i]])
            start = j+1

        return tcs

    def _fitting_TFIDF(self):
        summary = self.transcript['results']['transcripts'][0]['transcript'].split(".")
        import string
        table = str.maketrans('', '', string.punctuation)
        summary = [w.translate(table) for w in summary]

        vectorizer = TfidfVectorizer(stop_words = 'english')
        response = vectorizer.fit_transform(summary)
        tfidf = response.toarray().sum(axis=0)
        feature_names = vectorizer.get_feature_names()

        tfidf_per_word = {}
        for i, word in enumerate(feature_names):
            tfidf_per_word[word] = tfidf[i]

        #find a way to filter our summary with prettify
        tf_sentence = {}
        for sentences in summary:
            count = 0
            sentence_count = 0
            for words in sentences.split(" "):
                if words.lower() in tfidf_per_word:
                    count+=1
                    sentence_count += tfidf_per_word[words.lower()]

            tf_sentence[sentences] = sentence_count/(count+1)

        return [(k, tf_sentence[k]) for k in sorted(tf_sentence, key=tf_sentence.get, reverse=True)]
