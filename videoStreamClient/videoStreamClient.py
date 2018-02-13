import requests
import numpy as np
import cv2


def nd_arr(byte_string):
    nparr = np.fromstring(byte_string, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np


def get_stream():
    while True:
        try:
            # If the connection is established
            frame_bytes = requests.get('http://147.8.233.230:5000/stream', stream=True)
            if frame_bytes.status_code == 200:
                data = bytes()
                for chunk in frame_bytes.iter_content(chunk_size=1024):
                    data += chunk
                    a = data.find(b'\xff\xd8')
                    b = data.find(b'\xff\xd9')
                    if a != -1 and b != -1:
                        final_frame = data[a:b + 2]
                        data = data[b + 2:]
                        frame = nd_arr(final_frame)
                        cv2.imshow('Video feed', frame)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            exit(0)
        except requests.exceptions.ConnectionError:
            print("Could not connect")
            exit(0)


def main():
    get_stream()
    return 0


if __name__ == '__main__':
    main()
