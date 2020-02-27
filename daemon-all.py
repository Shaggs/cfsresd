"""cfsresd daemon
This version of cfsresd has been edited by @Shaggs to send pagers 
to Email, SMS and pushover.

this is based on original program by @adambrenecki


"""
from scraper import Scraper
import sys
import requests
from clint.textui import puts, colored
import urllib3
import serial
from time import sleep
import threading
import smtplib
from email.mime.text import MIMEText
import configparser
c = configparser.ConfigParser()
c.read('Settings.ini')
numbers = [ 
	x.strip()
	for x in c.get("SMS", "To").lower().split(",")
	]
usr = [ 
	x.strip()
	for x in c.get("PushOver", "To").lower().split(",")
	]

to = [ 
	x.strip()
	for x in c.get("Email", "To").lower().split(",")
	]
server = c.get("Email", "Server").lower()
urllib3.disable_warnings()

def email(msg):
	mesg = MIMEText ('%s - %s' % (msg.text, msg.channel))
	server = smtplib.SMTP(server)
	server.starttls()
	mesg['Subject'] = msg.channel
	mesg['From'] = ('From')
	mesg['To'] = str(to)
	server.login('username','password')
	server.sendmail(mesg.get('From'), emai, mesg.as_string())
	server.quit()
	print "email sent"
def sms(msg):
	if c.get("SMS", "COM") == "":
		print "No SMS Settings Found"
		return
	else:
		com = c.get("SMS", "COM")
		ser = serial.Serial(com, 460800, timeout=5)
		for x in range(0, len(msg.text), 150):
			for phone_number in numbers:
			ser.write('ATZ\r')
			sleep(1)
			ser.write('AT+CMGF=1\r')
			sleep(1)
			ser.write('AT+CMGS="%s"\r' % str(phone_number))
			sleep(1)
			ser.write(msg.text[x:x+150] + '\r' + chr(26))
			sleep(1)
			print "Sent message to %r:" % (phone_number)
def send(msg):
		app = ""# app ID
		for k in usr:
		user = k
		params = {
		'token': app,
		'user': user,
		'title': msg.channel,
		'message': msg.text,
		'retry': 30, 
		'expire': 180,
		'priority': 2 if msg.response else 0,
		}
		if msg.response: params['sound'] = 'updown'
		urllib3.disable_warnings()
		requests.post('https://api.pushover.net/1/messages.json', data=params, verify=False)
		name = usr[k]
		print "POSTed message to " + name
 
if __name__ == "__main__":
	scraper = Scraper(5, recent_messages=True)
	@scraper.register_handler
	def handler(msg)
	puts(" [", newline=False)
	puts(colored.green(msg.datetime), newline=False)
	puts("] ", newline=False)
	if msg.response:
			puts(colored.red(msg.text))
	else:
		puts(msg.text)
		# Copy and paste below as many times as you have filters 
		#---------------Start Here-----------------
		if '' in msg.channel: # add filter here 
			my_thread = threading.Thread(target=email, args=(msg,))
			my_thread2 = threading.Thread(target=sms, args=(msg,))
			my_thread3 = threading.Thread(target=send, args=(msg,))
			my_thread.start()
			my_thread2.start()
			my_thread3.start()
			my_thread.join()
			my_thread2.join()
			my_thread3.join()
			return
		#-------------Stop Here ------------------
		else:
			return
scraper.run()









