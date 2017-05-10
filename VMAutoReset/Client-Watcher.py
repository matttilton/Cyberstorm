import json
import os
import threading
import telnetlib
import sys

# import the config file
config_data = open('client.config').read()
config = json.loads(config_data)

def Watcher(num):
    os.system("inotifywait " + config["watchlist"][num] + ' --recursive')
    server = telnetlib.Telnet(config["host"], config["port"], config["timeout"])
    server.write('reset ' + str(config["name"]) + ' ' + str(config["watchlist"][num]))
    server.close()
    sys.exit()
    


threads = []
for i in range(len(config["watchlist"])):
    t = threading.Thread(target=Watcher, args=(i,))
    threads.append(t)
    t.start()
