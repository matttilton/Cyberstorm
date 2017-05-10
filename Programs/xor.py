
#Canes Venatici
#5-4-17

import sys
import fileinput

#Opens key file and reads
keyfile = open('key', 'r')
key = keyfile.read()

#Reads the incoming message
text = sys.stdin.read()

#xor function for xor the key and message
def xor(key, text):
    return "".join(chr(ord(x) ^ ord(y)) for x, y in zip(key, text))

#call the xor function and print the result
print(xor(key, text))

#close the key file
keyfile.close()
