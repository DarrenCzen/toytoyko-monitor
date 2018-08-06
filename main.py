import requests
import re
import time
import json
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style
from colorama import init
init(autoreset=True)

s = requests.Session()
requests.packages.urllib3.disable_warnings()

url = "https://www.toytokyo.com/new-arrivals/"

hookheaders = {'Content-Type': 'application/json'}
headers1 = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.91 Safari/537.36",
    }


r = s.get(url,headers=headers1,verify=False) # scrape productids and set standard for drop


soup = BeautifulSoup(r.text,"lxml")
#

slackwebhook = ""
discordwebhook = ""


products = []

word_list = ("Zombie Bunny") # add tuple of words here
print "Made by - https://twitter.com/thebotsmith"
print "\n"
print "Using {} as search criteria".format(word_list)

while len(products) == 0:
    r = s.get(url,headers=headers1,verify=False)
    results = soup.find_all("a",{"class":"product-item-image"})
    for result in results:
        if any(word in result['title'] for word in word_list):
            print (Fore.GREEN + "PRODUCTS FOUND")
            print (Fore.GREEN + result['href'] + "in Stock")
            products.append(result['title'])
            print "\n"

            #POST TO DISCORD
            jsondata = {"content":"presto in stock at {}".format(url)}
            r = requests.post(discordwebhook,json=jsondata,verify=False,headers=hookheaders)

            #POST TO SLACK
            messagepost = {"text":"prestos in stock at {}".format(url)}
            json_data = json.dumps(messagepost)
            req = requests.post(slackwebhook,data=json_data.encode('ascii'),headers={'Content-Type': 'application/json'},verify=False)

            #post to email

            smtp = smtplib.SMTP('smtp.gmail.com:587')
            smtp.ehlo()
            smtp.starttls()
            smtp.login("YOURGMAILRELAY","PASSWORD")
            msg = "presto in stock at {}".format(url)
            msgFrom = ("YOUR GMAIL RELAY")
            msgTo = ("SEND TO EMAIL")
            smtp.sendmail(msgFrom,msgTo,msg)

        else:
            print (Fore.RED + "did not find anything")
            time.sleep(5)
