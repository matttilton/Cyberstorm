import socket
import time
import sys
from binascii import unhexlify

ip = "138.47.102.193"
port = 31337

ONE = 0.05 # how much you need to wait 

# connct to the socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((ip, port))


# recieve data until you get a EOF in the message
covert_bin = ""
# read one byte at a time to prevent over saturation
data = s.recv(1)
while (data.rstrip("\n") != "EOF"):
	sys.stdout.write(data + " ")
	sys.stdout.flush()
	
	t0 = time.time()
	data = s.recv(1)
	t1 = time.time()
	
	delta = round(t1 - t0, 4)

	# stop if messages are sent too quickly
	if (delta == 0.0): 
		break
	if (delta >= ONE * 10):
		print("\nToo mcuh delay m8")
	if (delta >= ONE):
		covert_bin += "1"
	else:
		covert_bin += "0"


covert = ""
i = 0

# convert ascii bin to string
while (i < len(covert_bin)):
	# rip 8 1/0 at a time
	b = covert_bin[i:i+8]
	n = int("0b{}".format(b), 2)

	try:
		covert += unhexlify("{0:x}".format(n))
	except TypeError:
		covert += "?"
	i += 8

print ("\nThe covert message: '{}'".format( covert))
s.close()

