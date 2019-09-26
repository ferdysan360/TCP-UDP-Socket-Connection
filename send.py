from socket import *
from packet import *
from constant import *
from helper import *
from datetime import datetime
from math import *
import sys
import os

print("Input host:")
UDP_IP = input(">> ")
print("Input port:")
UDP_PORT = int(input(">> "))

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket(AF_INET, SOCK_DGRAM)
# sock.connect((UDP_IP, UDP_PORT))
sock.settimeout(5.0)

filepath = input("Input your filepath: ")

dateTimeObj = datetime.now()
id = int(dateTimeObj.strftime("%H%M%S"))

list_of_byte = []
with open(filepath, "rb") as f:
    byte = f.read(MAX_DATA_LENGTH)
    while byte:
        list_of_byte.append(byte)
        byte = f.read(MAX_DATA_LENGTH)

i = 0
packet_count = len(list_of_byte)

progress = 0
sys.stdout.write("[%s]" % (" " * 40))
sys.stdout.write("\b" * (41))
sys.stdout.flush()

filename = os.path.basename(filepath)
sock.sendto(filename.encode(), (UDP_IP, UDP_PORT))
ACTUAL_PORT = int(sock.recv(1024).decode())

while (i < packet_count):
    checksum = get_checksum(list_of_byte[i])
    if (i != packet_count-1):
        new_packet = packet(DATA, id, i, checksum, list_of_byte[i])
    else:
        new_packet = packet(FIN, id, i, checksum, list_of_byte[i])
    sock.sendto(new_packet.get_packet_byte(), (UDP_IP, ACTUAL_PORT))
    try:
        # byte_packet = ack_sock.recv(1024)
        byte_packet = sock.recv(1024)
        data_packet = decode_packet(byte_packet)
        type = data_packet.get_type()
        if ((i+1)/packet_count*100 > progress*2.5):
            sys.stdout.write("\b" * (progress+1))
            sys.stdout.write("[%s]" % (" " * 40))
            sys.stdout.write("\b" * (41))
            for m in range(progress):
                sys.stdout.write("█")
                sys.stdout.flush()
            progress = ceil((i+1)/packet_count*40)
        if (type == FIN_ACK):
            sys.stdout.write("\b" * (progress+1))
            sys.stdout.write("[%s]" % (" " * 40))
            sys.stdout.write("\b" * (41))
            for m in range(40):
                sys.stdout.write("█")
                sys.stdout.flush()
            print("\nFile sent successfully")
            break
        i += 1
    except:
        print("\nFailed at " + str(i))
        print("Trying again...")
        sys.stdout.write("[%s]" % (" " * 40))
        sys.stdout.write("\b" * (41))
        for m in range(progress):
            sys.stdout.write("█")
            sys.stdout.flush()

sock.close()
