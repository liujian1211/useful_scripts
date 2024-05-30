import binascii


hex_str = "CBD544363031444400000000000000000000000000"
byte_str = binascii.unhexlify(hex_str)
string = byte_str.decode("gbk").replace('\u0000', '')

print(string)