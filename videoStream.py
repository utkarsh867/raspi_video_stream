from flask import Flask, render_template, Response
from streamCam import VideoStream

app = Flask(__name__)


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/stream')
def get_video():
    return Response(gen(VideoStream()), mimetype='multipart/x-mixed-replace;boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
