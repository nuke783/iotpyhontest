from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage,TextSendMessage

import paho.mqtt.client as mqttClient
import time

temp = ""
humi = ""

def on_message(client, userdata, msg):
    global temp,humi
    print(msg.topic+" "+str(msg.payload))
    text_t_h = msg.payload.decode('UTF-8')
    t_and_h = text_t_h.split(',')
    temp = t_and_h[0]
    humi = t_and_h[1]


channel_secret = "e175c0d5d15f53e43513d242a99f3079"
channel_access_token = "sgYP1Hxujh+iEw6+25CQ99ib1DxLrbGSC+99IQcqHt3v8EzECXvQvLJqjcVatMOi0Pa2tgkON9//OpgoLH5OoHWSSFSDlZLPU7S+DcaCPIOLNxq6447AzFGhQgXfELZwM5MFxZ7J4hBHdNIg/9rlHgdB04t89/1O/w1cDnyilFU="

broker_address= "150.95.31.215"
port = 1884

client = mqttClient.Client("xxx") # Client ID
user = "test01" # Token
password = "pwd01" # Secret

client.username_pw_set(user, password=password)    
client.on_message = on_message

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except:
        pass
    
    return "Hello Line Chatbot"

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    global temp,humi
    text = event.message.text
    print(text)

    try:
        client.connect(broker_address, port=port)        
    except:
        print("Connection failed")
    
    if (text=="เปิดไฟ"):
        client.publish("@msg/led","ledon")
        text_out = "เปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="ปิดไฟ"):
        client.publish("@msg/led","ledoff")
        text_out = "ปิดไฟเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีแดง"):
        client.publish("@msg/color","red")
        text_out = "เปิดไฟสีแดงเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีเขียว"):
        client.publish("@msg/color","green")
        text_out = "เปิดไฟสีเขียวเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="สีน้ำเงิน"):
        client.publish("@msg/color","blue")
        text_out = "เปิดไฟสีน้ำเงินเรียบร้อยแล้ว"
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))

    if (text=="อุณหภูมิและความชื้น"):
        client.subscribe("@msg/t_h")
        client.loop_start()
        time.sleep(1.5) 
        client.loop_stop()
        if len(temp) > 0 and len(humi) > 0:
            text_out = "อุณหภูมิ " + temp + " ความชื้น " + humi
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=text_out))
                     
if __name__ == "__main__":          
    app.run()

