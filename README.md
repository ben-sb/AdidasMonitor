# AdidasMonitor

Python program to monitor the availability status of Adidas products. 
Supports Adidas UK, US, CA, AU, NL, DE, NZ, RU. 
Requires Python 3.6 or above

## SMS setup (optional)
* Signup for free trial account https://www.twilio.com/try-twilio
* Verify your account with the phone number you want to use
* Get a free trial number
* Save your SID and Auth token


## Config
* webhook - your Discord webhook 
* refresh_time - how often to refresh (in seconds)
* products - list of JSON objects to monitor, each with region and PID (supported regions are listed above)
* sms_sid - your Twilio SID **(leave as null if not using SMS support)**
* sms_auth - your Twilio auth token **(leave as null if not using SMS support)**
* twilio_number - the phone number you got from Twilio **(leave as null if not using SMS support)**
* your_number - your phone number **(leave as null if not using SMS support)**


## To Run
* Install requirements in requirements.txt
* Edit config.json
* Put proxies in proxies.txt or clear file to run without proxies
* Run main.py
