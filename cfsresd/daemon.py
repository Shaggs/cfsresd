"""cfsresd daemon

This daemon will send a Pushover notification for every pager message that is
for CFS Salisbury, Para Group or R2, excluding Officers, Ops and HQ channels.

It takes two command line arguments: the app ID and the user ID.
"""
from cfsresd.scraper import Scraper
import sys
import requests

if __name__ == "__main__":
    assert len(sys.argv) == 3
    app_token = sys.argv[1]
    user_token = sys.argv[2]

    scraper = Scraper(5, recent_messages=False)
    @scraper.register_handler
    def handler(msg):
        if 'CFS' not in msg.channel:
            return
        if ('Salisbury' not in msg.channel
            and 'Para Group' not in msg.channel
            and 'R2' not in msg.channel
            and 'Region 2' not in msg.channel):
            return
        if ('Officers' in msg.channel
            or 'Ops' in msg.channel
            or 'Operations Support' in msg.channel
            or 'HQ' in msg.channel
            or 'Headquarters' in msg.channel
            or 'Person' in msg.channel
            or 'John Hutchins' in msg.channel):
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
