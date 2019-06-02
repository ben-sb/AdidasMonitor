import requests
import json
import time
from threading import Thread
from dhooks import Webhook, Embed
from twilio.rest import Client
import random
from datetime import datetime

class AdidasMonitor():
    def __init__(self, region, pid, webhooks, refresh_time, sms_sid=None, sms_auth=None, twilio_number=None, client_number=None):
        self.region = region.lower()
        self.pid = pid
        self.webhooks = webhooks
        self.refresh_time = refresh_time
        self.count = 0
        self.latest_status = ""
        self.sizes = []
        self.proxies = []
        self.headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'upgrade-insecure-requests': '1',
                'user-agent': self.get_random_ua()
            }

        if sms_sid != None and sms_auth != None:
            self.sms_client = Client(sms_sid, sms_auth)
            self.twilio_number = twilio_number
            self.client_number = client_number
        else:
            self.sms_client = None

        self.load_region_data()
        self.load_proxies()


    def log(self, msg):
        print('[{}]: {}'.format(datetime.now(), msg))


    def load_proxies(self):
        self.proxies = open('proxies.txt').readlines()


    def get_random_ua(self):
        return random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36"
        ])


    def load_region_data(self):
        if self.region == "uk":
            self.domain = ".co.uk"
            self.country = "GB"
        elif self.region == "us":
            self.domain = ".com"
            self.country = "US"
        elif self.region == "ca":
            self.domain = ".ca"
            self.country = "CA"
        elif self.region == "au":
            self.domain = ".com.au"
            self.country = "AU"
        elif self.region == "nl":
            self.domain = ".nl"
            self.country = "NL"
        elif self.region == "de":
            self.domain = ".de"
            self.country = "DE"
        elif self.region == "nz":
            self.domain = ".co.nz"
            self.country = "NZ"
        elif self.region == "ru":
            self.domain = ".ru"
            self.country = "RU"
        else:
            self.log("Region not recognized")
            exit(1)

    def sanitize_status(self, status):
        return status.replace('_', ' ').title()


    def format_proxy(self, proxy):
        try:
            ip = proxy.split(":")[0]
            port = proxy.split(":")[1]
            userpassproxy = '%s:%s' % (ip, port)
            proxyuser = proxy.split(":")[2].rstrip()
            proxypass = proxy.split(":")[3].rstrip()
            proxies = {'http': 'http://%s:%s@%s' % (proxyuser, proxypass, userpassproxy),
                       'https': 'http://%s:%s@%s' % (proxyuser, proxypass, userpassproxy)}

        except:
            proxies = {'http': 'http://%s' % proxy, 'https': 'http://%s' % proxy}

        return proxies


    def get_stock_url(self):
        return 'https://www.adidas{}/api/products/{}/availability'.format(self.domain, self.pid)


    def get_wishlist_url(self):
        return "https://www.adidas{}/on/demandware.store/Sites-adidas-{}-Site/en_{}/Wishlist-GetColorVariation?cid={}".format(self.domain, self.country, self.country, self.pid)


    def start(self):
        t = Thread(target=self.monitor_thread)
        t.start()


    def monitor_thread(self):
        while True:
            stock_url = self.get_stock_url()

            try:
                if len(self.proxies) > 0:
                    stock = json.loads(requests.get(stock_url, headers=self.headers, proxies=self.format_proxy(random.choice(self.proxies)), timeout=10).text)
                else:
                    stock = json.loads(requests.get(stock_url, headers=self.headers, timeout=10).text)

                if 'availability_status' in stock:
                    status = stock['availability_status']

                    # check for new sizes being loaded, or sizes coming back into stock
                    altered_sizes = []
                    if 'variation_list' in stock:
                        for new_size in stock['variation_list']:

                            size_exists = False
                            for existing_size in self.sizes:
                                if new_size['size'] == existing_size['size']:
                                    size_exists = True

                                    if new_size['availability_status'] != existing_size['availability_status'] and new_size['availability_status'] == "IN_STOCK":
                                        altered_sizes.append(new_size)


                            if not size_exists:
                                altered_sizes.append(new_size)

                        self.sizes = stock['variation_list']


                    # detect change if overall status has changed or if there has been a change in available sizes
                    if status != self.latest_status or len(altered_sizes) > 0:
                        self.latest_status = status
                        if self.count > 0:
                            self.log("Detected status updated to %s" % self.latest_status)
                            self.send_to_discord(altered_sizes)
                            if self.sms_client != None:
                                self.send_text()

                        else:
                            self.log("Loaded initial status as %s"%self.latest_status)

                    else:
                        self.log("No update detected, current status is %s"%self.latest_status)
                else:
                    # detect product not loaded
                    if 'not found' in str(stock):
                        self.log("Product not loaded")
                    else:
                        self.log("No updates detected")
            except Exception as e:
                self.log("Error loading stock: " + str(e))


            self.count += 1
            time.sleep(self.refresh_time)


    def send_to_discord(self, altered_sizes):
        # create the embed
        embed = Embed(
            title = '%s on Adidas %s'%(self.pid, self.region.upper()),
            url = self.get_wishlist_url(),
            color = 10764258,
            timestamp = 'now'
        )

        # add embed fields
        embed.add_field(name='PID', value=self.pid)
        embed.add_field(name='Region', value=self.region.upper())
        embed.add_field(name='Overall Status', value=self.sanitize_status(self.latest_status), inline=False)

        # add the sizes to the embed
        for size in altered_sizes:
            embed.add_field(name='Size %s'%size['size'], value=self.sanitize_status(size['availability_status']), inline=True)

        # set the footer
        embed.set_footer(text='SD Adidas Monitor', icon_url='https://i.imgur.com/ceVbiGI.png')

        # send the embed to each webhook
        for webhook in self.webhooks:
            hook = Webhook(webhook)
            hook.username = "SD Adidas Monitor"
            hook.avatar_url = "https://pbs.twimg.com/profile_images/1001585704303030273/SNhhIYL8_400x400.jpg"
            hook.send(embed=embed)

        self.log("Posted status update to Discord")


    def send_text(self):
        try:
            self.sms_client.messages.create(to=self.client_number, from_=self.twilio_number, body="%s on Adidas %s\n%s"%(self.pid, self.region.upper(), self.get_wishlist_url()))
            self.log("Sent text message")
        except:
            self.log("Error sending text message")
