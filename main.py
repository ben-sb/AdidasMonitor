from classes.adidas_monitor import AdidasMonitor
import json

try:
    config = json.load(open('config.json'))

    webhook = config['webhook']
    refresh_time = config['refresh_time']
    pids = config['pids']

    for pid in pids:
        monitor = AdidasMonitor(pid, webhook, refresh_time)
        monitor.start()

# case where config file is missing
except FileNotFoundError:
    print("FATAL ERROR: Could not find config file")

# case where config file is not valid json
except json.decoder.JSONDecodeError:
    print("FATAL ERROR: Could not read config file, invalid JSON")


except Exception as e:
    print("Unknown error: " + str(e))