import socket
import logging
import threading
import time
import packet
from constant import *
from datetime import datetime

def receive_message(name):
    "Send message procedure (default)"
    global thread_count
    
    print("Waiting")
    conn, addr = sock.accept()
    dateTimeObj = datetime.now()
    timestampStr = dateTimeObj.strftime("%d-%b-%Y_(%H%M%S)")
    
    with open('received_file_' + timestampStr, 'wb') as f:
        print('receiving data packet...')
        while True:
            byte_packet = conn.recv(MAX_PACKET_LENGTH)
            data_packet = packet.decode_packet(byte_packet)
            type = data_packet.get_type()
            data = data_packet.get_data()
            
            if (type == FIN):
                print("File received successfully")
                ack = packet.packet(FIN_ACK,
                  data_packet.get_id(),
                  data_packet.get_seq_number(),
                  data_packet.get_checksum())
                conn.send(ack.get_packet_byte())
                f.write(data)
                break
            else:
                ack = packet.packet(ACK,
                  data_packet.get_id(),
                  data_packet.get_seq_number(),
                  data_packet.get_checksum())
                conn.send(ack.get_packet_byte())
            f.write(data)

    thread_count -= 1

print("Input port:")
UDP_PORT = (int) (input(">> "))

UDP_IP = "127.0.0.1"

sock = socket.socket()
sock.bind((UDP_IP, UDP_PORT))
sock.listen(5)

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
