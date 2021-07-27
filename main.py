# Original Author: smartbuilds.io
# Modified: Daniel Park
# Date: 7.12.21
# Desc: This script opens a video stream on a Private IP address of the Pi Camera

from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import os

# Create the Flask App
app = Flask(__name__)

# Move the frames on the screen
@app.route('/', methods=['GET', 'POST'])
def move():
    result = ""
    if request.method == 'POST':
        return render_template('index.html', res_str=result)
    return render_template('index.html')

# Run the camera
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# Open the video feed
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Run the web app
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
