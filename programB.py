import time
from socket import *
from sys import  *
import requests

from programA import buffer_size, offset

if len(argv) != 4:
    print("Error: wrong number of arguments")
    exit(1)

url = argv[1]
movie_name = argv[2]
results_file_name = argv[3]

addr, port = (url.split('/')[2]).split(':')

socket = socket(family=AF_INET, type=SOCK_STREAM)
socket.connect((addr, int(port)))

request = f"GET ./{movie_name}/manifest.txt HTTP/1.0\r\n\r\n"

socket.send(request.encode())

recv_data = socket.recv(buffer_size)

tmp = b''

while recv_data:
    tmp += recv_data
    recv_data = socket.recv(buffer_size)

tmp_str = tmp.decode()
header_end = tmp_str.find("\r\n\r\n")

if header_end == -1:
    print("Invalid HTTP")
    exit(1)

content = tmp_str[header_end + 4:]
lines = content.split("\n")

with open(results_file_name, "w") as rf:
    num_tracks = int(lines[1])
    num_seg = int(lines[6])

    movie_header = 2
    track_header = 5
    offset = movie_header + track_header
    track_name_line = movie_header

    for t in range(num_tracks):
        track_name = lines[track_name_line]
        url = f'http://{addr}:{port}/{movie_name}/{track_name}' # request url
        print(f'{url}\n')
        duration = 0
        for s in range(offset, offset + num_seg):
            seg = lines[s]
            seg_offset, seg_size = map(int, seg.split(" "))
            seg_end = seg_size + seg_offset - 1
            headers = {"Range" : f"bytes={seg_offset}-{seg_end}"} # request header
            start = time.time()
            # download
            video_data = requests.get(url, headers=headers)  # request
            end = time.time()
            duration += end - start

        rf.write(f'{str(duration)}\n')
        offset += track_header + num_seg # offset update
        track_name_line += num_seg + track_header





# print(content)

