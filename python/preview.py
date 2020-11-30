import hashlib
import subprocess



def open_ffplay(server_ip, stream_name, password):
    timestamp = '1923350399' #unix time 12/12/2030 @ 11:59pm (UTC) - expiration time
    sum = '/live/' + stream_name + '-' + timestamp + '-' + password
    calc_link = hashlib.md5(sum.encode('utf-8')).hexdigest()
    connection_link = 'rtmp://' + server_ip +'/live/' + stream_name + '?sign=' + timestamp + '-' + calc_link

    subprocess.Popen('C:/inz/ffmpeg/bin/ffplay.exe ' + connection_link)



