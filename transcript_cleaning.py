import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from transcription_job import *
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import word_tokenize
import string

class TranscriptCleaning:
    def __init__(self, status):
        self.status = status
        self.run()

    def get_word_tcs(self):
        # new_link = self.status['TranscriptionJob']['Transcript']['TranscriptFileUri']
        # self.transcript = pd.read_json(new_link)
        real_transcript = self.status['results']['items']
        tc_and_words = []
        for i in real_transcript:
            if 'start_time' in i.keys():
                tc_and_words.append([i['start_time'],i['end_time'],i['alternatives'][0]['content']])
        self.tc_words = tc_and_words
        return tc_and_words

    def get_transcript(self):
        self.transcript = self.status['results'][1][0]['transcript']
        return self.transcript

    def get_sentences_with_tcs(self):
        separated_sentences = self.transcript.split(" ")
        sentences_period = self.transcript.split(".")[0:-1]
        end_sentence = [i for i, word in enumerate(separated_sentences) if "." in word]

        tcs = []
        start = 0
        for i,j in enumerate(end_sentence):
            tcs.append([(self.tc_words[start][0],self.tc_words[j][-2]),sentences_period[i]])
            start = j+1
        self.sentence_tc = tcs
        return self.sentence_tc

    def sentence_cleaning(self):
        sentences_period = self.transcript.split(".")[0:-1]
        wordnet_lemmatizer = WordNetLemmatizer()
        stop = stopwords.words('english') +list(["i'm","it","i'll"])
        translator = str.maketrans('', '', string.punctuation)

        summary = []
        for sentences in sentences_period:
            summary.append(" ".join(
                                    [wordnet_lemmatizer.lemmatize(word.translate(translator))
                                    for word in sentences.lower().split(" ")
                                    if word not in stop]))
        return summary, [[self.sentence_tc[i][0],summary[i]] for i in range(len(summary))]

    def fit_TFIDF(self):
        vectorizer = TfidfVectorizer(stop_words = 'english')
        response = vectorizer.fit_transform(self.summary)
        tfidf = response.toarray().sum(axis=0)
        feature_names = vectorizer.get_feature_names()

        tfidf_per_word = {}
        for i, word in enumerate(feature_names):
            tfidf_per_word[word] = tfidf[i]

        tf_sentence = []
        for sentences in self.tc_and_clean:
            count = 0
            sentence_count = 0
            for words in sentences[1].split(" "):
                if words in tfidf_per_word:
                    count+=1
                    sentence_count += tfidf_per_word[words.lower()]

            tf_sentence.append([sentences,(sentence_count/(count+1))])

        return tf_sentence


    def run(self):
        self.tc_words = self.get_word_tcs()
        self.transcript = self.get_transcript()
        self.sentence_tc = self.get_sentences_with_tcs()
        self.summary, self.tc_and_clean = self.sentence_cleaning()
    # def _fitting_TFIDF(self):
    #     summary = self.transcript['results']['transcripts'][0]['transcript'].split(".")
    #     import string
    #     table = str.maketrans('', '', string.punctuation)
    #     summary = [w.translate(table) for w in summary]
    #
    #     vectorizer = TfidfVectorizer(stop_words = 'english')
    #     response = vectorizer.fit_transform(summary)
    #     tfidf = response.toarray().sum(axis=0)
    #     feature_names = vectorizer.get_feature_names()
    #
    #     tfidf_per_word = {}
    #     for i, word in enumerate(feature_names):
    #         tfidf_per_word[word] = tfidf[i]
    #
    #     #find a way to filter our summary with prettify
    #     tf_sentence = {}
    #     for sentences in summary:
    #         count = 0
    #         sentence_count = 0
    #         for words in sentences.split(" "):
    #             if words.lower() in tfidf_per_word:
    #                 count+=1
    #                 sentence_count += tfidf_per_word[words.lower()]
    #
    #         tf_sentence[sentences] = sentence_count/(count+1)
    #
    #     return [(k, tf_sentence[k]) for k in sorted(tf_sentence, key=tf_sentence.get, reverse=True)]
