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
    mp4s = [i for i in thumbnails  if i[-4::] == ".mp4"]
    jpegs = [i for i in thumbnails  if i[-4::] == ".jpg"]
    thumbnails = [file[0:-4] for file in jpegs]
    return render_template('landingPage.html', thumbnails = thumbnails)

@app.route('/new', methods =['POST'])
def new():
    link = request.form["link"]
    if not link:
        return "Submit a link!"
    model = Editor(link, bucket_name='hos123', run = True)
    new_entry = Database(model, run=True)
    model_info = new_entry.find_entry(model.title)

    outfile = open('session.pkl','wb')
    pickle.dump(model, outfile)
    outfile.close()
    return render_template('vid.html', vid_name=model.title[-4::], model_info=model_info)

@app.route('/vid/<string:vid_name>')
def vid(vid_name):
    new_entry = Database()
    model_info = new_entry.find_entry(vid_name+".mp4")
    return render_template('vid.html',vid_name=vid_name, model_info=model_info)


if __name__ == '__main__':
    app.run(use_reloader=True, debug = True)
