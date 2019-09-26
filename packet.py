SEP = '/|~}'.encode()

class packet:
  def __init__(self, type = None, id = None, seq_number = None, checksum = None, data = None):
    if not isinstance(type, bytes) and type != None:
      raise TypeError("type must be set to a byte")
    if not isinstance(id, int) and id != None:
      raise TypeError("id must be set to an integer")
    if not isinstance(seq_number, int) and seq_number != None:
      raise TypeError("seq_number must be set to an integer")
    self.type = type if (type) else 0
    self.id = id if (id) else 0
    self.seq_number = seq_number if (seq_number) else 0
    self.length = len(data) if (data) else 0
    self.checksum = checksum if (checksum) else 0
    self.data = data if (data) else b'0'

  # Setter
  def set_seq_number(self, seq_number):
    if not isinstance(seq_number, int):
      raise TypeError("seq_number must be set to an integer")
    self.seq_number = seq_number

  def set_length(self, length):
    if not isinstance(length, int) and length > 0:
      raise TypeError("length must be set to an unsigned integer")
    self.length = length

  def set_checksum(self, checksum):
    self.checksum = checksum

  def set_data(self, data):
    self.data = data

  # Getter
  def get_type(self):
    return self.type

  def get_id(self):
    return self.id

  def get_seq_number(self):
    return self.seq_number

  def get_length(self):
    return self.length

  def get_checksum(self):
    return self.checksum

  def get_data(self):
    return self.data

  def get_packet_byte(self):
    type_byte = self.type
    id_byte = str(self.id).encode()
    seq_number_byte = str(self.seq_number).encode()
    length_byte = str(self.length).encode()
    checksum_byte = self.checksum
    data_byte = self.data
    packet_byte = b"".join([type_byte, SEP,
        id_byte, SEP,
        seq_number_byte, SEP,
        length_byte, SEP,
        checksum_byte, SEP,
        data_byte])
    return packet_byte

  # Other Methods
  def print_debug(self):
    print("Type: " + str(self.type))
    print("ID: " + str(self.id))
    print("Seq Num: " + str(self.seq_number))
    print("Length: " + str(self.length))
    print("Checksum: " + str(self.checksum))
    print("Data: " + str(self.data))

# Helper Functions 
def decode_packet(byte_str):
    "Decodes byte into packet object"
    byte_arr = byte_str.split(SEP)
    if (len(byte_arr) != 6):
        print(len(byte_arr))
        print(byte_arr[0][:30])
    result_packet = packet(byte_arr[0],
        int(byte_arr[1].decode()),
        int(byte_arr[2].decode()),
        byte_arr[4],
        byte_arr[5])
    return result_packet
