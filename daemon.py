"""cfsresd daemon

This daemon will send a Pushover notification for every pager message that is
for your set requirments.

It takes two command line arguments: the app ID and the user ID.
"""
from scraper import Scraper
import sys
import requests

if __name__ == "__main__":
   app_token= "insert app token here "
   user_token = "insert user token here "
    scraper = Scraper(5, recent_messages=False)
    @scraper.register_handler
    def handler(msg):
        """ set CFS, SES or MFS"""
        if 'CFS' not in msg.channel:
            return
        """ type below the filters you would like to set"""
        
        if ('' not in msg.channel
            and '' not in msg.channel
            and '' not in msg.channel
            and '' not in msg.channel):
            return 
        """ type below the filters you would like to ignore"""
        
        if ('' in msg.channel
            or '' in msg.channel
            or '' in msg.channel
            or '' in msg.channel
            or '' in msg.channel
            or '' in msg.channel
            or '' in msg.channel):
            return

        params = {
            'token': app_token,
            'user': user_token,
            'title': msg.channel,
            'message': msg.text,
            'priority': 1 if msg.response else 0,
        }
        if msg.response: params['sound'] = 'siren'
        requests.post('https://api.pushover.net/1/messages.json', data=params)
        print "POSTed message"

    scraper.run()
