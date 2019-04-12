import sqlite3
import os

class Database:

    def __init__(self, model=None, run=False):
        self.con = sqlite3.connect("transcripts.db")
        self.model = model
        if run:
            self.run()

    def run(self):
        self.con
        self.add_entry()
        self.close_db()

    def create_db(self):
        c.execute('''CREATE TABLE transcripts (video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words);''')

    def close_db(self):
        self.con.commit()
        self.con.close()

    def convert_top_words(self):
        dict_words = self.model.tfidf_per_word
        top_words = sorted(dict_words.items(), key=lambda x: x[1], reverse = True)[0:20]
        top_words = ["".join(str(i)) for i in top_words]
        return " | ".join(top_words)

    def add_entry(self):
        video_id = self.model.title
        name_of_video = self.model.video_title
        Full_Transcript = self.model.transcript
        Cleaned_Transcript = ".".join(self.model.df.Sentence.values)
        Important_Words = self.convert_top_words()
        self.con.cursor().execute('''INSERT IGNORE INTO transcripts(video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words)
                    VALUES(?,?,?,?,?)''',(video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words))

    def find_entry(self, title):
        c = self.con.cursor()
        c.execute(''' SELECT * from transcripts where video_id = ?''',(title,))
        entry = c.fetchall()
        self.close_db()
        return entry
