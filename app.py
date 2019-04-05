from flask import Flask, render_template, request
from string import Template
app = Flask(__name__)



@app.route('/')
def homepage():

    return render_template('TESTVIDEO.html')

@app.route('/vid', methods =["POST"])
def videos():
    name = request.form["name"]

    return render_template('vid.html',name=name)


# @app.route('/videos/<vid>')
# def videos(vid):
    # vidtemplate = Template('''
    # <video width="320" height="240" controls>
    #     <source src="../Videos/${video_id}" type="video/mp4">
    #     <source src="movie.ogg" type="video/ogg">
    #     Your browser does not support the video tag.
    # </video>''')


    # vidtemplate.substitute(video_id = vid)
# @app.route('/video')
# def video():
#     return STATIC_MAP_TEMPLATE.substitute(place_name="full_vuln.mp4")

if __name__ == '__main__':
    app.run(use_reloader=True, debug = True)
