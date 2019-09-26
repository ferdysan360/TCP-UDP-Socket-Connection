from socket import *
import logging
import threading
import time
import packet
from constant import *
from helper import *

UDP_IP = "127.0.0.1" # localhost
port_list = [5000, 5001, 5002, 5003, 5004]

def receive_message(name):
    "Send message procedure (default)"
    global thread_count
    
    print("Waiting")
    data, addr = sock.recvfrom(1024)
    print("Address:", addr, data)
    ack_sock = socket(AF_INET, SOCK_DGRAM)
    ack_sock.connect((addr[0], addr[1]))

    port_used = port_list[0]
    port_list.remove(port_used)
    ack_sock.send(str(port_used).encode())
    server_sock = socket(AF_INET, SOCK_DGRAM)
    server_sock.bind((UDP_IP, port_used))

    filename = data.decode()
    
    with open('received_file/' + filename, 'wb') as f:
        print('receiving data packet...')
        while True:
            byte_packet, addr = server_sock.recvfrom(MAX_PACKET_LENGTH)
            data_packet = packet.decode_packet(byte_packet)
            type = data_packet.get_type()
            data = data_packet.get_data()
            checksum = get_checksum(data)
            ori_checksum = data_packet.get_checksum()
            
            if (checksum == ori_checksum):
                if (type == FIN):
                    print("File received successfully")
                    ack = packet.packet(FIN_ACK,
                      data_packet.get_id(),
                      data_packet.get_seq_number(),
                      ori_checksum)
                    ack_sock.send(ack.get_packet_byte())

                    f.write(data)
                    break
                else:
                    ack = packet.packet(ACK,
                      data_packet.get_id(),
                      data_packet.get_seq_number(),
                      ori_checksum)
                    ack_sock.send(ack.get_packet_byte())
                    f.write(data)
            else:
                print('cheksum error', checksum, ori_checksum)
    
    port_list.append(port_used)
    thread_count -= 1

print("Input port:")
UDP_PORT = (int) (input(">> "))

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))
# sock.listen(5)

# Concurrent process (Threading)
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    index = 0
    thread_count = 0

    while True:
        if (thread_count < 5):
            x = threading.Thread(target=receive_message, args=(index,))
            x.start()
            thread_count += 1
            print("Current Thread Count: " + str(thread_count))
