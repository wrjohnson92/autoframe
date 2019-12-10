from twilio.rest import Client
import sys
import config

if(len(sys.argv) == 2):
	print("setting up {0}".format(sys.argv[1]))
	client = Client(config.accountSid, config.authToken)

	incoming_phone_number = client.incoming_phone_numbers(config.phoneSid).update(
		sms_url = sys.argv[1] + "/sms"
	);