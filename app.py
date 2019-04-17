from flask import Flask, render_template, request
from string import Template
import os
from editing import *
from dbSQL import *
import pickle

app = Flask(__name__)

@app.route('/')
def homepage():
    thumbnails = os.listdir('static/videos')
    jpegs = [i for i in thumbnails  if i[-4::] == ".jpg"]
    thumbnails = [file[0:-4] for file in jpegs]
    vid_titles = []
    for i in thumbnails:
        new_entry = Database(run=False)
        model_info = new_entry.find_entry(i+'.mp4')
        vid_titles.append(model_info[0][1])
    new_titles = [(i,j) for i,j in zip(thumbnails,vid_titles)]

    return render_template('index.html', thumbnails = new_titles)

@app.route('/new', methods =['POST'])
def new():
    link = request.form["link"]
    if not link:
        return "Submit a link!"

    model = Editor(link, bucket_name='hos123', run = True)
    new_entry = Database(model, run=True)
    new_entry = Database(model, run=False)
    model_info = new_entry.find_entry(model.title)
    top_words = model_info[0][4].split("|")

    return render_template('vid.html', vid_name=model.title[:-4], model_info=model_info, top_words=top_words)

@app.route('/vid/<string:vid_name>')
def vid(vid_name):
    new_entry = Database()
    model_info = new_entry.find_entry(vid_name+".mp4")
    top_words = model_info[0][4].split("|")
    return render_template('vid.html',vid_name=vid_name, model_info=model_info, top_words=top_words)


if __name__ == '__main__':
    app.run(use_reloader=True, debug = True)
