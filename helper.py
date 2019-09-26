def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def get_checksum(data):
    byte_count = len(data)
    i = 0
    checksum = 0
        
    while (i < byte_count-1):
        checksum ^= ((data[i] << 8) + data[i+1])
        i += 2

    if (byte_count % 2 == 1):
        checksum ^= (data[i] << 8)

    checksum = b"".join([bytes([checksum & 0xFF]), bytes([(checksum >> 8) & 0xFF])])

    return checksum