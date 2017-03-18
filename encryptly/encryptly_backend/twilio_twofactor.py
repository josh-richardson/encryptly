import random
import string

from twilio.rest import TwilioRestClient

account_sid = "AC8e46e54e7c3b1eab7b0be72880db09d1"
auth_token = "bce322ca58f096efb04032c5abd14a31"
client = TwilioRestClient(account_sid, auth_token)


def random_string(n):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(n))


def send_text_message(message, number):
    client.messages.create(body=message,
                           to=number,
                           from_="+441133207262")
