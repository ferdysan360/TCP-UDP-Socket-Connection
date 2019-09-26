from socket import *
from constant import *
from helper import *
import logging
import threading
import time
import packet

UDP_IP = "127.0.0.1"  # localhost
port_list = [5000, 5001, 5002, 5003, 5004]
id_list = [0, 1, 2, 3, 4]


def receive_message(name, ID):
    "Send message procedure (default)"
    global thread_count

    print("Waiting for client (Thread %s)" % ID)
    data, addr = sock.recvfrom(1024)
    ack_sock = socket(AF_INET, SOCK_DGRAM)
    ack_sock.connect((addr[0], addr[1]))

    port_used = port_list[0]
    port_list.remove(port_used)
    ack_sock.send(str(port_used).encode())
    server_sock = socket(AF_INET, SOCK_DGRAM)
    server_sock.bind((UDP_IP, port_used))

    filename = data.decode()

    with open('received_file/' + filename, 'wb') as f:
        print('receiving data packet... (Thread %s)' % ID)
        while True:
            byte_packet, addr = server_sock.recvfrom(MAX_PACKET_LENGTH)
            data_packet = packet.decode_packet(byte_packet)
            type = data_packet.get_type()
            data = data_packet.get_data()
            checksum = get_checksum(data)
            ori_checksum = data_packet.get_checksum()

            if (checksum == ori_checksum):
                if (type == FIN):
                    print("File received successfully (Thread %s)" % ID)
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

    port_list.append(port_used)
    id_list.append(ID)
    thread_count -= 1


print("Input port:")
UDP_PORT = (int)(input(">> "))

sock = socket(AF_INET, SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))

# Concurrent process (Threading)
if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    index = 0
    thread_count = 0

    while True:
        if (thread_count < 5):
            x = threading.Thread(target=receive_message,
                                 args=(index, id_list[0]))
            id_list.remove(id_list[0])
            x.start()
            thread_count += 1
