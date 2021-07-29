import numpy
import cv2
import datetime
import sys
from flask import Flask,render_template,Response
app=Flask(__name__)

duration=40

cam=cv2.VideoCapture(0)
fourcc=cv2.VideoWriter_fourcc(*'MJPG')
out=cv2.VideoWriter('output6.avi',fourcc,20.0,(640,480))

now=datetime.datetime.now()
finish_time=now+ datetime.timedelta(seconds=duration)

def video_stream():
    while datetime.datetime.now()<finish_time:
        success,frame=cam.read()
        out.write(frame)
        if not success:
            break
        else:
            ret,buffer=cv2.imencode('.jpg',frame)
            frame=buffer.tobytes()
        yield(b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n')
    out.release()
    cam.release()


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video')
def video():
    return Response(video_stream(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__=='__main__':
    app.debug=True
    app.run()