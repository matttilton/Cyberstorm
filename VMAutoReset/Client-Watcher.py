import json
import os
import threading
import telnetlib
import sys
import time

# import the config file
config_data = open('client.config').read()
config = json.loads(config_data)

server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
server.write('snapshot ' + str(config["name"]) + ' initial')
server.close()

def Watcher(num):
    stat1 = os.popen('stat ' + config["watchlist"][num] + ' | grep 2017 | grep "Modify\|Change" ').read().rstrip()
    while(1):
        stat2 = os.popen('stat ' + config["watchlist"][num] + ' | grep 2017 | grep "Modify\|Change" ').read().rstrip()
        if stat1 != stat2:
            print 'File ' + config["watchlist"][num] + ' changed'
            server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
            server.write('reset ' + str(config["name"]) + ' ' + str(config["watchlist"][num]))
            server.close()
        time.sleep(1)

threads = []
for i in range(len(config["watchlist"])):
    t = threading.Thread(target=Watcher, args=(i,))
    threads.append(t)
    t.start()
