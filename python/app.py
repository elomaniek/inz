from flask import *
import subprocess
import os
import socket
import signal
import hashlib
from flask_cors import CORS
from flask import Flask
from contextlib import closing
import sys
from sys import exit

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
ffmpeg_process = None
start_stream = True


def get_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]

def get_local_ip():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    #local_ip = '10.1.11.45'
    return local_ip

def get_server_ip():
    server_ip = '10.1.11.45'
    return server_ip

def get_name():
    stream_name = 'stream'
    return stream_name

def get_password():
    password = 'test'
    return password


def create_link(server_ip, stream_name, password):
    timestamp = '1923350399' #unix time 12/12/2030 @ 11:59pm (UTC) - expiration time
    sum = '/live/' + stream_name + '-' + timestamp + '-' + password
    calc_link = hashlib.md5(sum.encode('utf-8')).hexdigest()
    full_link = 'rtmp://' + server_ip +'/live/' + stream_name + '?sign=' + timestamp + '-' + calc_link
    print(full_link)
    return full_link


def default_stream():
    global ffmpeg_process
    global server_ip
    global name
    global password
    global connection_link

    #subprocess.call("taskkill.exe /t /f /im ffmpeg.exe")
    ffmpeg_process = subprocess.Popen('C:/inz/ffmpeg/bin/ffmpeg.exe ' +
                        '-re -f vfwcap -i 0 ' +    #Get camera input: -f vfwcap -i 0    OR    test video: lavfi -i testsrc
                        '-c:v libx264 ' +               # Codec - H.264
                        '-b:v 1600k -preset ultrafast -c:a libfdk_aac -b:a 128k -g 25 '+
                        #'-vf scale=' + res +    # Resolution
                        #' -r ' + fps +            # FPS
                        ' -pix_fmt yuv420p ' +  #
                        '-f flv "' + connection_link  + ' live=true"'
                        )




@app.route('/<fps><res>', methods=['POST'])
def index(fps,res):
    global ffmpeg_process
    global server_ip
    global name
    global password
    global connection_link

    print(" ---- CLIICKED ---- ")
    data = request.get_json("data")
    fps =str(data['fps'])
    res =str(data['res'])

    if ffmpeg_process is not None:
        print("SENDING_SIGNAL")
        ffmpeg_process.send_signal( signal.CTRL_C_EVENT )
        print("SENT.. WAITING TO KILL FFMPEG")
        ffmpeg_process.wait()


    ffmpeg_process = subprocess.Popen('C:/inz/ffmpeg/bin/ffmpeg.exe ' +
                        '-re -f lavfi -i testsrc '+                 #Get camera input: -f vfwcap -i 0    OR test video: lavfi -i testsrc
                        '-c:v libx264 '+                            #Codec - H.264
                        '-b:v 1600k -preset ultrafast -b 900k -c:a libfdk_aac -b:a 128k -g 25 '+ #stream stats
                        '-vf scale=' + res +                        #Resolution
                        ' -r ' + fps +                              #FPS
                        ' -pix_fmt yuv420p ' +                   #
                        '-f flv "' + connection_link + ' live=true"'
                        )


    return 'Nothing to see here'


def handler(signal_received, frame):
    global ffmpeg_process
    # Handle any cleanup here
    print('SIGINT or CTRL-C detected. ', file=sys.stderror)
    if signal_received == signal.SIGTERM:
        if ffmpeg_process is not None:
            print("SENDING_SIGNAL")
            ffmpeg_process.send_signal(signal.CTRL_C_EVENT)
            print("SENT.. WAITING TO KILL FFMPEG")
            ffmpeg_process.wait()
        exit()




def launch():
    global start_stream
    if start_stream is True:
        default_stream() #starts stream with default camera setup
    app.run(host = local_ip)



if '--do-not-start-stream' in sys.argv:
    start_stream = False

signal.signal(signal.SIGINT, handler)
server_ip = get_server_ip()
name = get_name()
password = get_password()
connection_link = create_link(server_ip,name,password)
local_ip = get_local_ip()
launch()
