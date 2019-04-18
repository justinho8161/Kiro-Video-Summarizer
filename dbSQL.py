from moviepy.editor import VideoFileClip
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
        c = self.con.cursor()
        c.execute('''CREATE TABLE transcripts (video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words, Original_Duration, New_Duration, Duration_Difference, Full_Word_Count, New_Word_Count, Count_Difference);''')

    def close_db(self):
        self.con.commit()
        self.con.close()

    def convert_top_words(self):
        dict_words = self.model.tfidf_per_word
        top_words = sorted(dict_words.items(), key=lambda x: x[1], reverse = True)[0:20]
        top_words = ["".join(str(i)) for i in top_words]
        return " | ".join(top_words)

    def get_duration_vars(self, id):
        os.chdir('/home/justin/Downloads/Capstone/static/videos')
        clipDuration = VideoFileClip(id).duration
        duration = "{}:{}:{}".format(int(clipDuration/3600), int((clipDuration%3600)), int(clipDuration%60))

        newClipDuration = VideoFileClip(id[:-4]+'s.mp4').duration
        newDuration = "{}:{}:{}".format(int(newClipDuration/3600), int((newClipDuration/60)), int(newClipDuration%60))

        duration_difference = "{}".format(((clipDuration-newClipDuration)/clipDuration)*100)
        os.chdir('/home/justin/Downloads/Capstone')
        return duration, newDuration, duration_difference

    def get_word_counts(self, model):
        words = len(model.transcript.split(" "))
        new_words = len(".".join(model.df.Sentence.values).split(" "))
        word_difference = ((words-new_words)/words)*100
        return words, new_words, word_difference

    def add_entry(self):
        video_id = self.model.title
        name_of_video = self.model.video_title
        Full_Transcript = self.model.transcript
        Cleaned_Transcript = ".".join(self.model.df.Sentence.values)
        Important_Words = self.convert_top_words()
        Original_Duration, New_Duration, Duration_Difference = self.get_duration_vars(video_id)
        Full_Word_Count, New_Word_Count, Count_Difference = self.get_word_counts(self.model)

        self.con.cursor().execute('''INSERT OR IGNORE INTO transcripts(video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words, Original_Duration, New_Duration, Duration_Difference, Full_Word_Count, New_Word_Count, Count_Difference)
                    VALUES(?,?,?,?,?,?,?,?,?,?,?)''',(video_id, name_of_video, Full_Transcript, Cleaned_Transcript, Important_Words, Original_Duration, New_Duration, Duration_Difference, Full_Word_Count, New_Word_Count, Count_Difference))

    def find_entry(self, title):
        c = self.con.cursor()
        c.execute(''' SELECT DISTINCT * from transcripts where video_id = ?''',(title,))
        entry = c.fetchall()
        self.close_db()
        return entry
