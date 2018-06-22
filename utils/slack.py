from slacker import Slacker


def send_to_slack(message, token, channel):
    Slacker(token).chat.post_message(channel, message)
