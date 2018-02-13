from flask import Flask, render_template, Response
from streamCam import VideoStream

app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield frame


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def get_video():
    return Response(gen(VideoStream()), mimetype='application/octet-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
