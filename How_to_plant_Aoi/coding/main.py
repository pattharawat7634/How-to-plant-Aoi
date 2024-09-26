from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, ImageMessage
import os
import google.generativeai as genai
import json
import requests

API_KEY = '2d2aceb6784907982259211844276aa2'
LAT = 16.4419
LON = 102.8360
BASE_URL = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"

app = Flask(__name__)

# LINE Bot configuration
line_bot_api = LineBotApi('49OWRVMFEPUphOLl3iNBWbBnA25oonIMuu3Gjl4wlzgsdwrxXwOgYfQ8MJIkreoNVr6iDIFvBWfOerCXllSKLCvu3SO8b9aGFfirxF+H/eaYJa3La8AV6nW3osSTkrzV93xWE+QiOuWVTGoC6oM/BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b8ca496d4f97dede39ba2f519890989e')

# Google AI configuration
GOOGLE_AI_API_KEY = os.getenv('GOOGLE_AI_API_KEY')
if not GOOGLE_AI_API_KEY:
    raise ValueError("GOOGLE_AI_API_KEY environment variable is not set")

genai.configure(api_key=GOOGLE_AI_API_KEY)
model = genai.GenerativeModel('gemini-pro')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

@handler.add(FollowEvent)
def handle_follow(event):
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    welcome_message = f" {profile.display_name} Hello, My name is How to Plant Aoi "
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    if user_message == "weather":

    # Fetch weather data
        weather_data = requests.get(BASE_URL).json()
        
        if weather_data['cod']!= '404':
            main_data = weather_data['main']
            temperature = main_data['temp']
            humidity = main_data['humidity']
            
            weather_description = weather_data['weather'][0]['description']
            
            weather_message = f"Temperature: {temperature}°C\nHumidity: {humidity}%\nWeather description: {weather_description}"
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=weather_message)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="City not found.")
            )
    if user_message =="C.C.S. คืออะไร":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="C.C.S. ย่อมาจากคำว่า Commercial Cane Sugar เป็นระบบการคิดคุณภาพของอ้อย ซึ่งได้นำแบบอย่างมาจากระบบการซื้อขายอ้อยของประเทศออสเตรเลีย คำว่า C.C.S. หมายถึง ปริมาณของน้ำตาลที่มีอยู่ในอ้อย ซึ่งสามารถหีบสกัดออกมาได้เป็นน้ำตาลทรายขาวบริสุทธิ์ ซึ่งตามมาตรฐาน C.C.S. กำหนดวิธีคิดว่า ในระหว่างผ่านกรรมวิธีการผลิต ถ้ามีสิ่งที่ไม่บริสุทธิ์ที่ละลายอยู่ในน้ำอ้อย 1 ส่วน จะทำให้สูญเสียน้ำตาลไป 50% ของจำนวนสิ่งที่ไม่บริสุทธิ์ อ้อย 10 C.C.S. จึงหมายถึง เมื่อนำอ้อยมาผ่านกระบวนการผลิต จะได้น้ำตาลทรายขาวบริสุทธิ์ 10% ดังนั้น อ้อย 1 ตัน หรือ 1,000 กิโลกรัม จะได้น้ำตาลทรายขาวบริสุทธิ์ 100 กิโลกรัม")
        )
    if user_message == "สูตรการคิดคำนวณราคาอ้อยเป็นอย่างไร":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ราคาอ้อย = รายได้ส่วนที่ 1 + (รายได้ส่วนที่ 2 X ค่า ซี.ซี.เอส. ที่ได้) + รายได้จากกากน้ำตาล\nรายได้ส่วนที่ 1 = รายรับจากการขายน้ำตาลที่คิดตามน้ำหนัก (สัดส่วน ร้อยละ 40)\nรายได้ส่วนที่ 2 = รายรับจากการขายน้ำตาลที่คิดตามค่าความหวาน (สัดส่วน ร้อยละ 60)")
        )
    
    if user_message == "เงินเกี๊ยวหรือเงินบำรุงอ้อย":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="ในทางนิติกรรม คือ เงินมัดจำในการขายอ้อยล่วงหน้านั่นเอง โดยชาวไร่ทำสัญญาขายอ้อยให้โรงงานและโรงงานจ่ายเงินมัดจำเป็นเช็คล่วงหน้า ซึ่งชาวไร่มักนำไปขายลดกับธนาคารที่โรงงานมีเครดิตอยู่ แต่ก็มีชาวไร่บางรายที่เก็บเช็คไว้รอเข้าบัญชีเมื่อเช็คครบกำหนดในช่วงที่มีการส่งอ้อยเข้าโรงงาน สำหรับการให้เงินเกี๊ยวผ่านหัวหน้าโควตานั้น หัวหน้าโควตามักจะนำเงินเกี๊ยวไปปล่อยต่อให้ลูกไร่ของตนในลักษณะเดียวกัน")
        )

    else:
        try:
            response = model.generate_content(user_message)
            ai_response = response.text
        except Exception as e:
            print(f"Error calling Google AI API: {str(e)}")
            ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
        
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=ai_response)
        )
if __name__ == "__main__":
    app.run()
    

# AIzaSyBJFbQo5Y1u2V4OLWSC96r84NyxorolSNg

#https://ibb.co/6XnRJcM