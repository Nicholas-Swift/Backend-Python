from twilio.rest import TwilioRestClient

account_sid = "----------------------"
auth_token = "-----------------------"

client = TwilioRestClient(account_sid, auth_token)

message = client.messages.create(
	to = "+----------",
	from_= "+-----------",
	body = "Text Here")

"""
NOTES:

# Get infomration!
Nick$ curl https://api.twilio.com/2010-04-01/Accounts/-----------------------/Messages.json -u ----------------------:-------------------- | python -m json.tool

# Send a text!
Nick$ curl -X POST https://api.twilio.com/2010-04-01/Accounts/-------------------/Messages.json -u ----------------------------:----------------------------- --data-urlencode 'From=+12062072038' --data-urlencode 'To=+12067084245' --data-urlencode 'Body=Hello from API class' | python -m json.tool

"""

print(message.sid)
