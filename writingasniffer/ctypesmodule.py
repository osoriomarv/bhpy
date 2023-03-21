from ctypes import *
import socket
import struct

class IP(Structure):
    _fields_ = [
        ("ihl", c_ubyte, 4), #4 bit unsigned char
        ("version", c_ubyte, 4), # 4 bit unsigned char
        ("tos", c_ubyte, 8), #1 byte  
        ("len", c_ushort, 16), #2 bytes unsigned short
        ("id", c_ushort, 16), #2 bytes unsigned short
        ("offset", c_ushort, 16), #2 bytes unsigned short
        ("ttl", c_ubyte, 8), #1 byte
        ("protocol_num", c_ubyte, 8), #1 byte
        ("sum", c_ushort, 16), #2 bytes unsigned short
        ("src", c_uint, 32), #4 bytes unsigned int
        ("dst", c_uint, 32) #4 bytes unsigned int
    ]

    def __new__(self, socket_buffer=None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer=None):
        # human readable IP addresses
        self.src_address = socket.inet_ntoa(struct.pack("@I", self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("@I", self.dst))
