from datetime import datetime

from slackclient import SlackClient

import helpers
import myconfigurations as config

try:
    slack_token = config.SLACK_TOKEN
    channel_name = config.SLACK_CHANNEL.replace("#", "")
    date_from = '2018-10-10 00:00:00'
    date_to = '2018-10-13 23:59:59'
    date_parsed_format = "%Y-%m-%d %H:%M:%S"

    oldest = (datetime.strptime(date_from, date_parsed_format) - datetime(1970, 1, 1)).total_seconds()
    latest = (datetime.strptime(date_to, date_parsed_format) - datetime(1970, 1, 1)).total_seconds()

    sc = SlackClient(slack_token)
    sc2 = SlackClient(config.SLACK_TOKEN_PRI)

    users_list = sc.api_call("users.list")
    users = {}
    for user in users_list['members']:
        users[user['id']] = user['profile']['real_name']

    channels = sc.api_call("channels.list")
    channel_id = None
    for channel in channels['channels']:
        if channel['name'] == channel_name:
            channel_id = channel['id']
            continue
    if channel_id == None:
        raise Exception("Cannot find channel " + channel_name)

    history = sc2.api_call("channels.history", channel=channel_id, oldest=oldest, latest=latest, count=50)
    posts_by_user = {}

    try:
        if history['error']:
            raise Exception("ERROR GETTING MESSAGE HISTORY: " + history['error'])
    except Exception as e:
        pass
except Exception as e:
    type, fname, lineno = helpers.getFormattedException()
    message = helpers.multiplyEmoji(":x:", 3) + "ERROR: {} \n{} {} {}".format(e, type, fname, lineno)
    print(message)
    helpers.postMessage(message)

def getMessages():
    return history['messages']
