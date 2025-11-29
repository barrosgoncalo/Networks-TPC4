import os
from socket import *
from sys import *

# python3 programA.py serverURL movieName resultsFileName
# ARGS: programA.py serverURL movieName resultsFileName

buffer_size = 1024

if len(argv) != 4:
    print("Error: wrong number of arguments")
    exit(1)

url = argv[1]
movie_name = argv[2]
results_file_name = argv[3]

addr, port = (url.split('/')[2]).split(':')

socket = socket(family=AF_INET, type=SOCK_STREAM)
socket.connect((addr, int(port)))

request = f'GET ./{movie_name}/manifest.txt HTTP/1.0\r\n\r\n'

socket.send(request.encode())

rcvd_data = socket.recv(buffer_size)

# manifest.txt file download

tmp = b'' # tmp variable

while rcvd_data:
    tmp += rcvd_data
    rcvd_data = socket.recv(buffer_size)

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
    rf.write(f"{num_tracks}\n{num_seg}\n")
    total = 0
    movie_header = 2
    track_header = 5
    offset = movie_header + track_header

    for t in range(num_tracks):
        total = 0
        for s in range(offset, offset + num_seg - 1):
            total += int(lines[s].split(" ")[1])
        rf.write(f"{total}\n")
        offset += track_header + num_seg


