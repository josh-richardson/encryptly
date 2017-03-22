from channels import Group
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.sessions import channel_session


# @channel_session
def http_consumer(message):
    # Make standard HTTP response - access ASGI path attribute directly
    response = HttpResponse("Hello world! You asked for %s" % message.content['path'])
    # Encode that response into message format (ASGI)
    for chunk in AsgiHandler.encode_response(response):
        message.reply_channel.send(chunk)


@channel_session
def ws_message(message):
    print("received")
    Group("chat-%s" % message.channel_session['room']).send({
        "text": message.content['text']
    })


@channel_session
def ws_connect(message):
    message.reply_channel.send({"accept": True})
    room = message.content['path'].strip("/")
    message.channel_session['room'] = room
    print("chat-%s" % room)
    Group("chat-%s" % room).add(message.reply_channel)


@channel_session
def ws_disconnect(message):
    Group("chat-%s" % message.channel_session['room']).discard(message.reply_channel)
