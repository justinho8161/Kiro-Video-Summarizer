from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer


class Model_Analysis:
    def __init__(self,transcript):
        self.stop_words = transcript.stop_words
        self.tc_words = transcript.tc_words
        self.transcript = transcript.transcript
        self.sentence_tc = transcript.sentence_tc
        self.summary, self.tc_and_clean = transcript.summary, transcript.tc_and_clean
        self.tfidf_per_word = None


    def fit_TFIDF(self):
        vectorizer = TfidfVectorizer(stop_words = 'english')
        response = vectorizer.fit_transform(self.summary)
        tfidf = response.toarray().sum(axis=0)
        feature_names = vectorizer.get_feature_names()

        self.tfidf_per_word = {}
        for i, word in enumerate(feature_names):
            self.tfidf_per_word[word] = tfidf[i]

        tf_sentence = []
        for idx, sentences in enumerate(self.tc_and_clean):
            count = 0
            sentence_count = 0
            for words in sentences[1].split(" "):
                if words in self.tfidf_per_word:
                    count+=1
                    sentence_count += self.tfidf_per_word[words.lower()]

            tf_sentence.append([self.sentence_tc[idx][0],self.sentence_tc[idx][1],sentences[1],(sentence_count/(count+1))])

        return tf_sentence
