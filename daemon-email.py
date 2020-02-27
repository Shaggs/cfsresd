"""cfsresd
This version of cfsresd has been edited by @Shaggs to send pagers 
to Email.

this is based on original program by @adambrenecki
"""
from scraper import Scraper
import sys
import requests
from clint.textui import puts, colored
import urllib3
import smtplib
from email.mime.text import MIMEText
if __name__ == "__main__":
	
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
		mesg = MIMEText ('%s - %s' % (msg.text, msg.channel))
		server = smtplib.SMTP('smtp details')
		server.starttls()
		mesg['Subject'] = msg.channel
		mesg['From'] = ('From')
		mesg['To'] = ('Person1@mail.com, person2@mail.com')
		server.login('username','password')
		server.sendmail(mesg.get('From'), emai, mesg.as_string())
		server.quit()
		print "email sent"
	scraper.run()