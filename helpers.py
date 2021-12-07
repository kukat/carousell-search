import os
import sys

from discord import Webhook, RequestsWebhookAdapter
from myconfigurations import DISCORD_WEBHOOK_URL

# import chatbot_slack as robot

def multiplyEmoji(emojiStr, multi):
    return emojiStr + "x %d" % multi

def postMessage(msg, img_url=""):
    print(msg)
    webhook = Webhook.from_url(DISCORD_WEBHOOK_URL, adapter=RequestsWebhookAdapter())
    webhook.send(msg) 
    # if msg:
        # robot.post_message(msg, img_url)

def getFormattedException():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno