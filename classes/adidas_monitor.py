import requests
import json
import time
from threading import Thread
from dhooks import Webhook, Embed
import random
from datetime import datetime


class AdidasMonitor():
    def __init__(self, pid, webhook, refresh_time):
        self.pid = pid
        self.webhook = webhook
        self.refresh_time = refresh_time
        self.count = 0
        self.latest_status = ""
        self.proxies = []
        self.headers = {
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
            }
        self.load_proxies()


    def log(self, msg):
        print('[{}]: {}'.format(datetime.now(), msg))


    def load_proxies(self):
        self.proxies = open('proxies.txt').readlines()
        self.log("Loaded %d proxies"%len(self.proxies))


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


    def start(self):
        t = Thread(target=self.monitor_thread)
        t.start()


    def monitor_thread(self):
        while True:
            stock_url = 'https://www.adidas.co.uk/api/products/{}/availability'.format(self.pid)

            try:
                if len(self.proxies) > 0:
                    stock = json.loads(requests.get(stock_url, headers=self.headers).text, proxies=self.format_proxy(random.choice(self.proxies)))
                else:
                    stock = json.loads(requests.get(stock_url, headers=self.headers).text)

                if 'availability_status' in stock:
                    status = stock['availability_status']
                    if status != self.latest_status:
                        self.latest_status = status
                        if self.count > 0:
                            self.log("Detected status updated to %s" % self.latest_status)
                            self.send_to_discord()
                        else:
                            self.log("Loaded initial status as %s"%self.latest_status)

                    else:
                        self.log("No update detected, current status is %s"%self.latest_status)
                else:
                    if 'not found' in str(stock):
                        self.log("Product not loaded")
                    else:
                        self.log("No updates detected")
            except:
                self.log("Error loading stock")


            self.count += 1
            time.sleep(self.refresh_time)


    def send_to_discord(self):
        hook = Webhook(self.webhook)

        embed = Embed(
            description='Status update on %s' % self.pid,
            color=0x1e0f3,
            timestamp='now'
        )

        embed.add_field(name='Status', value=self.latest_status)
        embed.set_footer(text='SD Adidas Monitor', icon_url='https://i.imgur.com/ceVbiGI.png')
        hook.send(embed=embed)
        self.log("Posted status update to Discord")





