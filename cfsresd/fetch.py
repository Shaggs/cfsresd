import requests
import lxml.html as lh
import sys

API_URL = "http://urgmsg.net/livenosaas/ajax/update.php"

SERVICE = 'CFS'
BRIGADE = 'Salisbury'
GROUP = 'Para Group'

def fetch_filtered(id):
	next, results = fetch_since(id)
	filtered_results = []
	for r in results:
		if SERVICE not in r['channel']:
			continue
		if BRIGADE not in r['channel']:
			if GROUP not in r['channel'] or 'Officers' in r['channel']:
				continue
		r['response'] = '*CFSRES' in r['msg']
		filtered_results.append(r)
	return next, filtered_results

def fetch_since(id):
	resp = requests.get(API_URL, params={'f': id}).json()
	if not resp['updated']:
		return id, []
	else:
		frags = lh.fragments_fromstring(resp['data'])
		return resp['IDstamp'], [_get_dict_from_fragment(x) for x in frags]

def _get_dict_from_fragment(fragment):
	r = {}
	children = fragment.getchildren()
	r['date'] = children[0].text
	r['msg'] = children[1].text
	# channel starts with `- `
	r['channel'] = children[1].getchildren()[0].text[2:]
	return r

if __name__ == "__main__":
	code, results = fetch_filtered(sys.argv[1] if len(sys.argv) > 1 else 1714006)
	for i in results:
		if i['response']:
			print '!!! RESPONSE MESSAGE !!!'
		print i['date']
		print i['channel']
		print i['msg']
		print
	print "Next Request:", code