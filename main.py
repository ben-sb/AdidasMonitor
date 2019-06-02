# written by SD
# twitter.com/ciphersuites

from classes.adidas_monitor import AdidasMonitor
import json

try:
    config = json.load(open('config.json'))

    webhooks = config['webhooks']
    refresh_time = config['refresh_time']
    products = config['products']

    sms_sid = config['sms_sid']
    sms_auth = config['sms_auth']
    twilio_number = config['twilio_number']
    client_number = config['your_number']

    print("Loaded %d proxies"%len(open('proxies.txt').readlines()))
    for product in products:
        monitor = AdidasMonitor(product['region'], product['pid'], webhooks, refresh_time, sms_sid, sms_auth, twilio_number, client_number)
        monitor.start()

# case where config file is missing
except FileNotFoundError:
    print("FATAL ERROR: Could not find config file")

# case where config file is not valid json
except json.decoder.JSONDecodeError:
    print("FATAL ERROR: Could not read config file, invalid JSON")

# case where we don't know the cause of the exception
except Exception as e:
    print("Unknown error: " + str(e))