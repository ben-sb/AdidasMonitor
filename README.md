# AdidasMonitor

Requires Python 3.6 or above

## SMS setup
* Signup for free trial account https://www.twilio.com/try-twilio
* Verify your account with the phone number you want to use
* Get a free trial number
* Save your SID and Auth token


## Config
* webhook - your Discord webhook 
* refresh_time - how often to refresh (in seconds)
* products - list of JSON objects to monitor, each with region and PID (note only Adidas UK, US and CA are supported currently)
* sms_sid - your Twilio SID
* sms_auth - your Twilio auth token
* twilio_number - the phone number you got from Twilio
* your_number - your phone number


## To Run
* Install requirements in requirements.txt
* Edit config.json
* Put proxies in proxies.txt
* Run main.py
