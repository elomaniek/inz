import hashlib
import subprocess

def create_link(server_ip, stream_name, password):
    timestamp = '1923350399' #unix time 12/12/2030 @ 11:59pm (UTC) - expiration time
    sum = '/live/' + stream_name + '-' + timestamp + '-' + password
    calc_link = hashlib.md5(sum.encode('utf-8')).hexdigest()
    full_link = 'rtmp://' + server_ip +'/live/' + stream_name + '?sign=' + timestamp + '-' + calc_link
    print(full_link)
    return full_link

def open_ffplay():
    global connection_link
    ffplay_process = subprocess.Popen('C:/inz/ffmpeg/bin/ffplay.exe ' + connection_link)

#open_ffplay()

def get_server_ip():
    server_ip = '10.1.11.45'
    return server_ip

def get_name():
    stream_name = 'stream'
    return stream_name

def get_password():
    password = 'password'
    return password

server_ip = get_server_ip()
name = get_name()
password = get_password()
connection_link = create_link(server_ip, name, password)
