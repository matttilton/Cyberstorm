import socket
import sys
import json
import os

# import the config file
config_data = open('config.json').read()
config = json.loads(config_data)

# Constant declaration
HOST = ''
PORT = config["port"]
BUFFER_SIZE = config["buffersize"]
BLACKLISTFILENAME = config["blacklist"]
WHITELISTFILENAME = config["whitelist"]

# Redirect output to log file. The 0 stops python from buffering the output.
sys.stdout = open(config["log"], "a", 0)

# Declare black and whitelist arrays
BLACKLIST = []
WHITELIST = []

# Populate blacklist
BLACKLISTFILE = open(BLACKLISTFILENAME, 'a+')
BLACKLISTFILE.seek(0)
for line in BLACKLISTFILE:
    print line.rstrip() + ' found in blacklist file. Blacklisting.'
    BLACKLIST.append(line.rstrip())
BLACKLISTFILE.close()
    
# Populate whitelist
WHITELISTFILE = open(WHITELISTFILENAME, 'a+')
WHITELISTFILE.seek(0)
for line in WHITELISTFILE:
    print line.rstrip() + ' found in whitelist file. Whitelisting.'
    WHITELIST.append(line.rstrip())
BLACKLISTFILE.close()

def addToBlackList(addr):
    if addr not in WHITELIST and addr not in BLACKLIST:
        BLACKLIST.append(addr)
        with open(config["blacklist"], "a") as BLACKLISTFILE:
            BLACKLISTFILE.write(addr)
        BLACKLISTFILE.close()
        print 'Blacklisted ' + addr + ' for invalid response.'

def addToWhiteList(addr):
    if addr not in BLACKLIST and addr not in WHITELIST:
        WHITELIST.append(addr)
        with open(config["whitelist"], "a") as WHITELISTFILE:
            WHITELISTFILE.write(addr)
        WHITELISTFILE.close()
        print 'Whitelisted ' + addr + '. first response was valid.'

def handleServerReset(addr, conn, data):
    dataArray = data.rstrip().split(' ')
    conn.close()
    if dataArray[0] == 'reset' and dataArray[1] in config["vm-names"]:
        addToWhiteList(addr[0])
        commands = ["VBoxManage controlvm " + dataArray[1] + " poweroff", 
                    "VBoxManage snapshot " + dataArray[1] + " restore " + config["snapshots"][dataArray[1]],
                    "VBoxManage showvminfo " + dataArray[1] + " | grep State >> ~/virtualboxLogs.log",
		            "VBoxHeadless -s " + dataArray[1] + " &"]
        for command in commands:
            if os.system(command) == 0:
                continue
            else:
                if command != commands[0]:
                    print 'Error restarting ' + dataArray[1]
                    break
                else:
                    print dataArray[1] + ' not on. Ignoring and continuing.'
                    continue
    else:
        addToBlackList(addr[0])
        conn.send('If you were not previously whitelisted, you have been blacklisted for sending an invalid request. Contact server admin.')
        conn.close()

# Create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to bind socket
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print "Failed to bind socket."
    sys.exit()

# Start listening with maximum queue of 5
s.listen(5)
print 'Listening on port ' + str(PORT) + '...'

# Server logic
try:
    while 1:
        conn, addr = s.accept()
        data = conn.recv(BUFFER_SIZE)
        if not data:
            print 'connection from ' + addr[0] + ' terminated unexpectedly.'
        else:
            if addr[0] in WHITELIST and addr[0] in BLACKLIST:
                BLACKLIST.remove(addr[0])
            if addr[0] not in BLACKLIST:
                handleServerReset(addr, conn, data)
            else:
                print 'Connection attempt from blacklisted device ' + addr[0]
                conn.send('This device has been Blacklisted. Contact server admins.')
                conn.close()
except KeyboardInterrupt:
    print '\r'
    sys.exit()
except EOFError:
    print('\r')
    sys.exit()
s.close()
