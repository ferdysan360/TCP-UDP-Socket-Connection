from socket import *
from packet import *
from constant import *
from helper import *
from math import *
from datetime import datetime
import sys
import os


def update_progress_bar(progress):
    sys.stdout.write("\b" * (progress+1))
    sys.stdout.write("[%s]" % (" " * 40))
    sys.stdout.write("\b" * (41))
    for m in range(progress):
        sys.stdout.write("█")
        sys.stdout.flush()


print("Input host:")
UDP_IP = input(">> ")
print("Input port:")
UDP_PORT = int(input(">> "))

sock = socket(AF_INET, SOCK_DGRAM)
sock.settimeout(5.0)

filepath = input("Input your filepath: ")

dateTimeObj = datetime.now()
id = int(dateTimeObj.strftime("%H%M%S"))

list_of_byte = []
try:
    with open(filepath, "rb") as f:
        byte = f.read(MAX_DATA_LENGTH)
        while byte:
            list_of_byte.append(byte)
            byte = f.read(MAX_DATA_LENGTH)
except:
    print("Filepath not valid")
    exit()

filename = os.path.basename(filepath)
try:
    sock.sendto(filename.encode(), (UDP_IP, UDP_PORT))
    ACTUAL_PORT = int(sock.recv(1024).decode())
except:
    print("Something went wrong")
    exit()

i = 0
packet_count = len(list_of_byte)
progress = 0

while (i < packet_count):
    checksum = get_checksum(list_of_byte[i])
    if (i != packet_count-1):
        new_packet = packet(DATA, id, i, checksum, list_of_byte[i])
    else:
        new_packet = packet(FIN, id, i, checksum, list_of_byte[i])
    sock.sendto(new_packet.get_packet_byte(), (UDP_IP, ACTUAL_PORT))
    try:
        byte_packet = sock.recv(1024)
        data_packet = decode_packet(byte_packet)
        type = data_packet.get_type()
        if ((i+1)/packet_count*100 > progress*2.5):
            update_progress_bar(progress)
            progress = ceil((i+1)/packet_count*40)
        if (type == FIN_ACK):
            update_progress_bar(40)
            print("\nFile sent successfully")
            break
        i += 1
    except:
        print("\nFailed at " + str(i))
        print("Trying again...")
        update_progress_bar(progress)

sock.close()
