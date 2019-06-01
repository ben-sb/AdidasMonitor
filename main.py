from classes.adidas_monitor import AdidasMonitor
import json

try:
    config = json.load(open('config.json'))

    webhook = config['webhook']
    refresh_time = config['refresh_time']
    products = config['products']

    sms_sid = config['sms_sid']
    sms_auth = config['sms_auth']
    twilio_number = config['twilio_number']
    client_number = config['your_number']

    for product in products:
        monitor = AdidasMonitor(product['region'], product['pid'], webhook, refresh_time, sms_sid, sms_auth, twilio_number, client_number)
        monitor.start()

# case where config file is missing
except FileNotFoundError:
    print("FATAL ERROR: Could not find config file")

# case where config file is not valid json
except json.decoder.JSONDecodeError:
    print("FATAL ERROR: Could not read config file, invalid JSON")


except Exception as e:
    print("Unknown error: " + str(e))