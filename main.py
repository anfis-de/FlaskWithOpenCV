#!/usr/bin/env python3

#-*- coding:utf-8 -*-

import cv2
from flask import Flask, render_template, Response

app = Flask(__name__) # define app

class Videocamera:
    """
    Provides functionality of given camera
    """
    def __init__(self, src):
        self.cap = cv2.VideoCapture(src)
    
    def getFrames(self):
        """
        read capture and return byte_img if sucessfull
        """
        ret, frame = self.cap.read()
        if ret:
            suc, jpeg = cv2.imencode(".jpg", frame)
            return suc, jpeg.tobytes()
        else:
            self.cap.release()
            return ret, None

def getCamera(cam):
    """
    read frames from camera in loop
    """
    while True:
        ret, frame = cam.getFrames()
        if ret:
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
        else:
            break

@app.route('/')
def index():
    """
    show landing page
    """
    return render_template('index.html')

@app.route('/cam0')
def getCam0():
    """
    show barebone video stream of camera0
    """
    src = getCamera(Videocamera(0))
    return Response(src,
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port='7000', debug=True) # run app at given address
