from time import sleep
import io
import cv2
from picamera import PiCamera
import numpy as np
import time

from matrixing_image import ImageToMatrix
from image_clear_noise import clearNoise
import nine_point_localization

# remember to close camera!
def open_preview():
    with PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.start_preview()
        sleep(5)


def image_process(image):
    clearNoise(image, 30, 4, 3)
    img = ImageToMatrix(image)
    x_label, y_label, now = nine_point_localization.local_positioning(img)
    return x_label, y_label, now


def capture_images_and_processing():
    """
    keep capturing images; quality unknown
    :return:
    """
    start_time = time.time()
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        sleep(1)

        stream = io.BytesIO()
        for foo in camera.capture_continuous(stream, format='jpeg', use_video_port=True):
            data = np.fromstring(stream.getvalue(), dtype=np.uint8)
            image = cv2.imdecode(data, cv2.IMREAD_COLOR)   #  can we use IMREAD_GRAYSCALE instead?

            #cv2.imshow("img", image)

            x_positioning, y_positioning, now = image_process(image)
            print("x_position:",x_positioning)
            print("y_position:", y_positioning)
            print("runtime:", now - start_time)

            # Truncate the stream to the current position (in case
            # prior iterations output a longer image)

            stream.truncate()
            stream.seek(0)

if __name__ == '__main__':
    capture_images_and_processing()

