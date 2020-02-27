import requests
import lxml.html as lh
import sys
import time
from clint.textui import puts, colored

API_URL = "http://urgmsg.net/livenosaas/ajax/update.php"

class Scraper (object):
	id_stamp = 0

	def __init__(self, timeout, recent_messages=True):
		self.timeout = timeout
		self.handlers = []
		self.recent_messages = recent_messages

	def register_handler(self, handler):
		self.handlers.append(handler)
		return handler

	def scrape(self):
		try:
			resp = requests.get(API_URL, params={'f': self.id_stamp}).json()
		except requests.exceptions.ConnectionError as e:
			puts("Error encountered when connecting to urgmsg: ", newline=False)
			puts(colored.magenta(e.__class__.__name__), newline=False)
			print ""
			time.sleep(self.timeout)
			scraper.run()

		if not resp['updated']:
			return

		old_id_stamp = self.id_stamp
		self.id_stamp = resp['IDstamp']
		# if old_id_stamp is 0, this is the first scrape
		# which will return a whole bunch of recent past messages
		if not self.recent_messages and old_id_stamp == 0: return

		# Pager messages are returned newest to oldest, we want to
		# process them oldest to newest
		frags = lh.fragments_fromstring(resp['data'])[::-1]
		for frag in frags:
			msg = PagerMessage(frag)
			for handler in self.handlers:
				handler(msg)

	def run(self):
		while True:
			self.scrape()
			time.sleep(self.timeout)

class PagerMessage:
	def __init__(self, fragment):
		children = fragment.getchildren()
		self.datetime = children[0].text
		self.text = children[1].text
		# channel starts with `- `
		self.channel = children[1].getchildren()[0].text[2:]
		self.response = 'CFSRES' in self.text
	def __str__(self):
		return "{} [{}]: {}".format(self.channel, self.datetime, self.text)

if __name__ == "__main__":
	scraper = Scraper(5)
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
	scraper.run()
