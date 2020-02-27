"""cfsresd
This version of cfsresd has been edited by @Shaggs to send pagers 
to SMS.

this is based on original program by @adambrenecki
"""
from scraper import Scraper
import sys
import requests
from clint.textui import puts, colored
import urllib3
import serial
import time
ser = serial.Serial('COM3', 460800, timeout=5)
if __name__ == "__main__":
	numbers['123456789', '1234567789'] #Add mobile numbers here as a list
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
		if 'CFS' not in msg.channel: # Add agancy here e.g CFS, SES, MFS
			return
		if ('' not in msg.channel # add Filter here e.g Bridgewater (Will look for Info and Response)
			and '' not in msg. # More filters
			and '' not in msg.channel
			and '' not in msg.channel
			and '' not in msg.channel):
			return
		if ('Ops' in msg.channel # add things we want to skip e.g this will skip STURT GROUP OPS if Sturt Group is set above
			or 'Operations Support' in msg.channel
			or 'Officers Response' in msg.channel
			or 'Officers Info' in msg.channel
			or 'HQ' in msg.channel
			or 'Headquarters' in msg.channel
			or 'Person' in msg.channel
			or 'John Hutchins' in msg.channel):
			return
		for x in range(0, len(msg.text), 150):
			for phone_number in numbers:
			ser.write('ATZ\r')
			time.sleep(1)
			ser.write('AT+CMGF=1\r')
			time.sleep(1)
			ser.write('AT+CMGS="%s"\r' % str(phone_number))
			time.sleep(1)
			ser.write(msg.text[x:x+150] + '\r' + chr(26))
			time.sleep(1)
			print "Sent message to %r:" % (phone_number)
	scraper.run()