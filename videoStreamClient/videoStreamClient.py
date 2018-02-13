from flask import Flask, Response, render_template
import requests
import imageConversions as ic
import cv2

app = Flask(__name__)


def get_stream():
    while True:
        frame_bytes = requests.get('http://localhost:5000/stream', stream=True)
        if frame_bytes.status_code == 200:
            data = bytes()
            for chunk in frame_bytes.iter_content(chunk_size=1024):
                data += chunk
                a = data.find(b'\xff\xd8')
                b = data.find(b'\xff\xd9')
                if a != -1 and b != -1:
                    final_frame = data[a:b + 2]
                    data = data[b + 2:]
                    frame = ic.nd_arr(final_frame)
                    cv2.imshow('Video feed', frame)
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        exit(0)


@app.route('/')
def index():
    main()


@app.route('/stream')
def get_video():
    return Response(get_stream(), mimetype='multipart/x-mixed-replace;boundary=frame')


def main():
    get_stream()
    return 0


if __name__ == '__main__':
    main()
