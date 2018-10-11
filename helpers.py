import os
import sys

import chatbot_slack as robot

def multiplyEmoji(emojiStr, multi):
    temp = ""
    for count in range(0, multi):
        temp += emojiStr
    return temp

def postMessage(msg, img_url=""):
    if msg:
        robot.post_message(msg, img_url)

def getFormattedException():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return exc_type, fname, exc_tb.tb_lineno