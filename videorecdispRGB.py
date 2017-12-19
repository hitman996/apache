#!/usr/bin/python
# -*- coding: ascii -*-
import numpy as np
import cv2
import sys
import time
import signal
from flask import Flask, render_template, Response
from camera import VideoCamera
import cv2

app = Flask(__name__)

def frame_converter_to_bytes(frame):
    ret, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

@app.route('/')
def index():
    return render_template('index2.html')

def gen(camera):
    cap = cv2.VideoCapture(0)

    cv2.namedWindow('Original')

    while (True):
        # Capture frame-by-frame
        [ret, frame] = cap.read()

        # Display the resulting frame
        cv2.imshow('Original', frame)
        frame = frame_converter_to_bytes(frame)
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    # while True:
    #     frame = camera.get_frame()
    #     yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


# while(True):
#     # Capture frame-by-frame
#     [ret, frame] = cap.read()
#
#     # Display the resulting frame
#     cv2.imshow('Original',frame)
#     #yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# When everything done, release the capture
# cap.release()
# cv2.destroyAllWindows()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)