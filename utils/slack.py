from slacker import Slacker

def send_to_slack(message, token, channel):
	Slacker(token).chat.postMessage(channel, message,)
