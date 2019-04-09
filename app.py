from flask import Flask, render_template, request
from string import Template
import os
app = Flask(__name__)


thumbnails = os.listdir('static/imgs')
thumbnails = [file[0:-5] for file in sorted(thumbnails)]

@app.route('/')
def homepage():
    return render_template('TESTVIDEO.html', thumbnails = thumbnails)

@app.route('/vid/<string:vid_name>')
def vid(vid_name):

    return render_template('vid.html',vid_name=vid_name)


if __name__ == '__main__':
    app.run(use_reloader=True, debug = True)
