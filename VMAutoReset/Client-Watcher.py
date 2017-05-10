import json
import os

# import the config file
config_data = open('config.json').read()
config = json.loads(config_data)

for file in config["watchlist"]:
    os.system()