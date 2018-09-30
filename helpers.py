import chatbot_slack as robot

def multiplyEmoji(emojiStr, multi):
    temp = ""
    for count in range(0, multi):
        temp += emojiStr
    return temp

def postMessage(msg, img_url=""):
    if msg:
        robot.post_message(msg, img_url)