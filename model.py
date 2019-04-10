from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import numpy as np
from sklearn.metrics import jaccard_similarity_score
from scipy.spatial.distance import pdist, squareform
import pandas as pd

class Model_Analysis:
    def __init__(self,transcript):
        self.stop_words = transcript.stop_words
        self.tc_words = transcript.tc_words
        self.transcript = transcript.transcript
        self.sentence_tc = transcript.sentence_tc
        self.summary, self.tc_and_clean = transcript.summary, transcript.tc_and_clean

        self.tfidf_per_word = None
        self.tf_sentence = None
        self.df = None

    def fit_TFIDF(self):
        vectorizer = TfidfVectorizer(stop_words = 'english',ngram_range = (1,2), min_df = .01, max_df = .9, binary = True)
        response = vectorizer.fit_transform(self.summary)
        tfidf = response.toarray().sum(axis=0)
        feature_names = vectorizer.get_feature_names()

        self.tfidf_per_word = {}
        for i, word in enumerate(feature_names):
            self.tfidf_per_word[word] = tfidf[i]

        self.tf_sentence = []
        for idx, sentences in enumerate(self.tc_and_clean):
            count = 0
            sentence_count = 0
            for words in sentences[1].split(" "):
                if words in self.tfidf_per_word:
                    count+=1
                    sentence_count += self.tfidf_per_word[words.lower()]

            self.tf_sentence.append([self.sentence_tc[idx][0][0],self.sentence_tc[idx][0][1],
                                    float(self.sentence_tc[idx][0][1])-float(self.sentence_tc[idx][0][0]),
                                    self.sentence_tc[idx][1],sentences[1],(sentence_count/(count+1))])

        return self

    def construct_df(self):

        df = pd.DataFrame(self.tf_sentence, columns = ['TimeIn','TimeOut','Duration','Sentence','Cleaned_Sentence', 'TFIDF'])
        self.df = df[(df['TFIDF']>df['TFIDF'].mean()) & ((df['Cleaned_Sentence'].str.count(' ')+1)>3)]
        return self.df

    def test(self):
        vect = CountVectorizer(ngram_range = (1,2), min_df = .01, max_df = .9, binary = True)
        new_vect = vect.fit_transform(self.summary).toarray()
        squareform(pdist(new_vect, metric='jaccard')).shape
