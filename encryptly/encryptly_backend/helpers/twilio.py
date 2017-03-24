import random
import string

from twilio.rest import TwilioRestClient

# Filesystem is used to prevent sensitive info being pushed to GitHub
account_sid = "AC8e46e54e7c3b1eab7b0be72880db09d1"
auth_token = open("twilio.txt", "r").read().strip()
client = TwilioRestClient(account_sid, auth_token)


# Send a text message to a user.
def send_text_message(message, number):
    client.messages.create(body=message, to=number, from_="+441133207262")
