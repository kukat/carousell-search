from slackclient import SlackClient
from myconfigurations import SLACK_TOKEN, SLACK_CHANNEL

slack_notifier = SlackClient(SLACK_TOKEN)

api="chat.postMessage"
username="CarousellBot"
icon_emoji=":robot_face:"

def post_message(msg, img_url=""):
    if img_url:
        slack_notifier.api_call(
            api,
            channel=SLACK_CHANNEL,
            username=username,
            icon_emoji=icon_emoji,
            text=msg,
            attachments=[{"title": "###IMAGE###", "image_url": img_url}],
        )
    else:
        slack_notifier.api_call(
            api,
            channel=SLACK_CHANNEL,
            username=username,
            icon_emoji=icon_emoji,
            text=msg,
        )
    print("Slack message POSTED successfully!")