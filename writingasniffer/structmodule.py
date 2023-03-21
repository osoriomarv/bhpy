import ipaddress
import struct

# EXAMPLE OF USING THE STRUCT MODULE TO PARSE PACKETS
# This is a simple example of using the struct module to parse packets

class IP:
    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.version = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4] 
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        # human readable IP addresses
        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        # MAP protocol constants to their names

        self.protocol_map = {1: "ICMP", 6: "TCP", 17: "UDP"}


