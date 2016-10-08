import httplib2
import urllib
import json
import base64


# Twilio Constants
class TwilioSMSAPI:

	# Variables
	BASE_URL = "https://api.twilio.com"
	PATH_URL = "/language/translate/v2"

	# Init
	def __init__(self, account_sid, auth_token):
		self.account_sid = account_sid
		self.auth_token = auth_token

	def __request(self, _from, to, text):
		user_and_pass = base64.b64encode(str(self.account_sid) + ':' + str(self.auth_token)).decode('ascii')
		text = text.encode('utf-8')

		# Set up parameters for request
		url = TwilioSMSAPI.BASE_URL + "/2010-04-01/Accounts/" + self.account_sid + "/Messages.json"
		headers = {'Accept-Charset': 'utf-8',
				   'Content-Type': 'application/x-www-form-urlencoded',
				   'Accept': 'application/json',
				   'User-Agent': 'twilio-python/5.6.0 (Python 2.7.10)',
				   'Authorization' : 'Basic ' + str(user_and_pass)}
		data = urllib.urlencode({'Body': text, 'From': _from, 'To': to})

		# post request
		http = httplib2.Http()
		response, content = http.request(url, "POST", headers=headers, body=text)

		return((response, content))

	def send(self, _from, to, text):
		response, content = self.__request(_from, to, text)
		return(response, content)


if __name__ == "__main__":
	main()
