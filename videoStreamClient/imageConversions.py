import numpy as np
import cv2


def nd_arr(byte_string):
    nparr = np.fromstring(byte_string, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return img_np
