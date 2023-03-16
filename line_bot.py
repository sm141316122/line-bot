from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


app = Flask(__name__)

line_bot_api = LineBotApi('97bL0MQKMDV+q4E5lpM2HsG+4PENFvZ2VwuJGywCztT8V81g5VH03z9g1lLXrFE4G6KMPsRYlSi1QPy\
    b8D/x0WYvxh9k4C1UPp3+RdwnNaatDHUost/gwapy7NBIVRjdmrKgHGZs7px6jhMMMQYRiwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18a0634ec65b34fc2c9318c8bdf2d867')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()