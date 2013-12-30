import requests
import lxml.html as lh
import sys
import time
from clint.textui import puts, colored

API_URL = "http://urgmsg.net/livenosaas/ajax/update.php"

class Scraper (object):
	id_stamp = 0 # TODO: somehow get an initial value

	def __init__(self, timeout):
		self.timeout = timeout
		self.handlers = []

	def register_handler(self, handler):
		self.handlers.append(handler)
		return handler

	def scrape(self):
		resp = requests.get(API_URL, params={'f': self.id_stamp}).json()

		if not resp['updated']:
			return

		self.id_stamp = resp['IDstamp']

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
		self.response = '*CFSRES' in self.text
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
