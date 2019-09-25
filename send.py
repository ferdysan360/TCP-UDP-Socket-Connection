from socket import *
from packet import *
from constant import *
from helper import *
from datetime import datetime
import sys

print("Input host:")
UDP_IP = input(">> ")
print("Input port:")
UDP_PORT = int(input(">> "))

print("UDP target IP:", UDP_IP)
print("UDP target port:", UDP_PORT)

sock = socket(AF_INET, SOCK_STREAM)
sock.connect((UDP_IP, UDP_PORT))
sock.settimeout(5.0)

filepath = input("Input your filepath: ")

dateTimeObj = datetime.now()
id = int(dateTimeObj.strftime("%H%M%S"))

list_of_byte = []
data_xor = 0
with open(filepath, "rb") as f:
    byte = f.read(MAX_DATA_LENGTH)
    while byte:
        data_xor = byte
        list_of_byte.append(byte)
        byte = f.read(MAX_DATA_LENGTH)
        # data_xor = byte_xor(data_xor, byte)

i = 0
checksum = byte_xor(data_xor, ONES)
packet_count = len(list_of_byte)

progress = 0
sys.stdout.write("[%s]" % (" " * 40))
sys.stdout.write("\b" * (41))

while (i < packet_count):
    if (i != packet_count-1):
        new_packet = packet(DATA, id, i, 0, list_of_byte[i])
    else:
        new_packet = packet(FIN, id, i, 0, list_of_byte[i])
    sock.send(new_packet.get_packet_byte())
    try:
        byte_packet = sock.recv(1024)
        data_packet = decode_packet(byte_packet)
        type = data_packet.get_type()
        if (i/packet_count*100 > progress*2.5):
            sys.stdout.write("█")
            sys.stdout.flush()
            progress += 1
        if (type == FIN_ACK):
            print("\nFile sent successfully")
            break
        i += 1
    except:
        print("\nFailed at " + str(i))
        print("Trying again...")
        sys.stdout.write("[%s]" % (" " * 40))
        sys.stdout.write("\b" * (41))
        for i in range(progress):
            sys.stdout.write("█")
            sys.stdout.flush()

sock.close()
