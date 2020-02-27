"""cfsresd daemon

This daemon will send a Pushover notification for every pager message that is
for your requirements

"""
from scraper import Scraper
import sys
import requests
from clint.textui import puts, colored
print "Starting"
print "Monitoring"

if __name__ == "__main__":
    app_token = '' "Add App token here (made at pushover.net)"
    user_token = '' "Add User token here your device (or group made at pushover.net)"
    scraper = Scraper(5, recent_messages=True)
    @scraper.register_handler
    def handler(msg):
	puts(colored.yellow(msg.channel), newline=False)
	puts(" [", newline=False)
	puts(colored.green(msg.datetime), newline=False)
	puts("] ", newline=False)
	if msg.response:
			puts(colored.red(msg.text))
	else:
		puts(msg.text)
        if '' not in msg.channel: """" Put CFS SES MFS Here depending on what you want"""
            return
        if ('' not in msg.channel """" Add Filters here that you want sent"""
            and '' not in msg.channel
            and '' not in msg.channel
            and '' not in msg.channel
            and '' not in msg.channel):
            return
			
        if ('' in msg.channel """Add filters here you want skipped"""
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
            'priority': 2 if msg.response else 0,
            'retry': 30,
            'expire': 180,
            'sound': 'siren',
        }
        if msg.response: params['sound'] = 'updown'
        requests.post('https://api.pushover.net/1/messages.json', data=params)
        print "Message sent"
        print "Monitoring"

scraper.run()