# AdidasMonitor

Python program to monitor the availability status of Adidas products. 
Supports Adidas UK, US, CA, AU, NL, DE, NZ, IT, CZ, DK, FR, ES, BE, CH, MY, BR, SG, RU.
Requires Python 3.6 or above

## SMS setup (optional)
* Signup for free trial account https://www.twilio.com/try-twilio
* Verify your account with the phone number you want to use
* Get a free trial number
* Save your SID and Auth token


## Config
* webhooks - list of your Discord webhooks (as strings) 
* refresh_time - how often to refresh (in seconds)
* products - list of JSON objects to monitor, each with region and PID (supported regions are listed above)
* sms_sid - your Twilio SID **(leave as null if not using SMS support)**
* sms_auth - your Twilio auth token **(leave as null if not using SMS support)**
* twilio_number - the phone number you got from Twilio **(leave as null if not using SMS support)**
* your_numbers - list of your phone numbers (as strings) **(leave as null if not using SMS support)**

**Everything should be a string (surrounded by ") other than refresh_time**


## To Run
* Download and run the appropriate Python installer from here https://www.python.org/downloads/release/python-367/ (skip this step if you already have Python 3.6 installed)
* Install requirements in requirements.txt using one of the following commands
  - Windows: pip install -r requirements.txt
  - Mac and Linux: python3 -m pip install -r requirements.txt
* Edit config.json
* Put proxies in proxies.txt or clear file to run without proxies
* Run main.py using using one of the following commands
  - Windows: python main.py
  - Mac and Linux: python3 main.py
