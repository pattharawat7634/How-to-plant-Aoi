from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, ImageSendMessage ,FlexSendMessage
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


image_map = {
    "ccs": 'https://drive.google.com/uc?id=1VNB-9mzqXqvt0Ro2hfNYMkkYCgAkkGxb',
    "เงินเกี๊ยวคืออะไร": 'https://drive.google.com/uc?id=14GLf-KOZ4jctCiSmWplcI9Bqyqq3Perm',
    "เปรียบเทียบวัตถุดิบผลิตเอทานอล": 'https://drive.google.com/uc?id=1Qn5TogUY0mn5muo5zaKq1zzVFGihGWCV',
    "การแก้ไขปัญหาภัยแล้งของชาวไร่อ้อย": 'https://drive.google.com/uc?id=1PjKH0I9NPNl9fc-fD_DsG3_hh-rD18Hw',
    "การซื้อขายอ้อยตามค่าความหวาน": 'https://drive.google.com/uc?id=1iGNXN8aQETdmRrC2AvoGBqgzV_6e2ANr',
    "จำนวนโรงงานน้ำตาลผลิตเอทานอล": 'https://drive.google.com/uc?id=19ZvcYZMXB74GBhkvfu_beEkHclC7Yn7F',
    "น้ำตาลโควตา ก ข ค คืออะไร": 'https://drive.google.com/uc?id=1TdFQZ0rrvSWV-rn2c94RbsdFPKXBStwX',
    "มูลค่าการผลิตและรายได้ของอุตสาหกรรมอ้อยและน้ำตาลทรายของไทย": 'https://drive.google.com/uc?id=14PZq26Hm9Kurq5IQcK6Blm8apPxHzSnI',
    "ราคาน้ำตาลทรายภายในประเทศ": 'https://drive.google.com/uc?id=1tGPquiVsHzERt_3HK2WZbkXHHUmvoOBC',
    "สภาวะการผลิตอ้อยและน้ำตาลทรายในอดีตถึงปัจจุบัน": 'https://drive.google.com/uc?id=10RdO54AavK8pXpybGm-3HZ65kIVPt47-',
    "สูตรการคำนวณราคาอ้อย": 'https://drive.google.com/uc?id=1QZ7NqQFb58uXYX9Sx-Oxcq1OE8GHHW3Z',
    "หัวหน้ากลุ่มชาวไร่อ้อยหัวหน้าโควตา": 'https://drive.google.com/uc?id=1ROiHj7I57OYgGbNJQcnFpx2yFhhQ8GpK',
    "องค์กรและสถาบันชาวไร่อ้อยและโรงงานน้ำตาล": 'https://drive.google.com/uc?id=1LxoRAR0_Va1SbApmqA8wYF5mq-5dWah5',
    "พระราชบัญญัติอ้อยและน้ำตาลทรายพ.ศ.2527มีเนื้อหาโดยสรุปอย่างไร": 'https://drive.google.com/uc?id=1tEARsEwijnn3E5I-Z0Cx8Hc-tYDfvVtF',
    "พันธุ์อ้อยที่สำนักงานคณะกรรมการอ้อยและน้ำตาลทรายแนะนำ": 'https://drive.google.com/uc?id=15w0DzEvepbDJMb0YnEwEwLcTTyoz4Air'
}
image_map_keys = {
    "ccs": "ccs",
    "ccsคือ": "ccs",
    "อะไรคือccs": "ccs",
    "ccsย่อมาจากอะไร": "ccs",
    "c.c.s.": "ccs",

    "อะไรคือเงินเกี๊ยว": "เงินเกี๊ยวคืออะไร",
    "เงินเกี๊ยวคืออะไร": "เงินเกี๊ยวคืออะไร",

    "เปรียบเทียบวัตถุดิบผลิตเอทานอล": "เปรียบเทียบวัตถุดิบผลิตเอทานอล",

    "เเก้ปัญหาภัยเเล้ง": "การแก้ไขปัญหาภัยแล้งของชาวไร่อ้อย",
    "ภัยเเล้งไร่อ้อย": "การแก้ไขปัญหาภัยแล้งของชาวไร่อ้อย",
    "ไร่อ้อยเเล้ง": "การแก้ไขปัญหาภัยแล้งของชาวไร่อ้อย",
    "ไร่อ้อยเเล้งทำไง": "การแก้ไขปัญหาภัยแล้งของชาวไร่อ้อย",

    "การซื้อขายอ้อยตามค่าความหวาน": "การซื้อขายอ้อยตามค่าความหวาน",
    "ซื้อขายตามค่าความหวาน": "การซื้อขายอ้อยตามค่าความหวาน",
    "ซื้อตามค่าความหวาน": "การซื้อขายอ้อยตามค่าความหวาน",
    "ขายตามค่าความหวาน": "การซื้อขายอ้อยตามค่าความหวาน",

    "จำนวนโรงงานเอทานอล": "จำนวนโรงงานน้ำตาลผลิตเอทานอล",
    "โรงงานผลิตเอทานอลในไทย": "จำนวนโรงงานน้ำตาลผลิตเอทานอล",
    "จำนวนโรงงานน้ำตาล": "จำนวนโรงงานน้ำตาลผลิตเอทานอล",
    
    "น้ำตาลโควตา": "น้ำตาลโควตา ก ข ค คืออะไร",
    "โควตาน้ำตาล": "น้ำตาลโควตา ก ข ค คืออะไร",
    
    "อุตสาหกรรมอ้อยและน้ำตาล": "มูลค่าการผลิตและรายได้ของอุตสาหกรรมอ้อยและน้ำตาลทรายของไทย",
    "มูลค่าการผลิตอ้อย": "มูลค่าการผลิตและรายได้ของอุตสาหกรรมอ้อยและน้ำตาลทรายของไทย",

    "ราคาน้ำตาลทราย": "ราคาน้ำตาลทรายภายในประเทศ",
    "ราคาน้ำตาลในประเทศ": "ราคาน้ำตาลทรายภายในประเทศ",

    "สภาวะการผลิตอ้อย": "สภาวะการผลิตอ้อยและน้ำตาลทรายในอดีตถึงปัจจุบัน",
    "ประวัติการผลิตอ้อย": "สภาวะการผลิตอ้อยและน้ำตาลทรายในอดีตถึงปัจจุบัน",

    "คำนวณราคาอ้อย": "สูตรการคำนวณราคาอ้อย",
    "วิธีคำนวณราคาอ้อย": "สูตรการคำนวณราคาอ้อย",

    "หัวหน้าโควตาอ้อย": "หัวหน้ากลุ่มชาวไร่อ้อยหัวหน้าโควตา",
    "ผู้นำกลุ่มชาวไร่อ้อย": "หัวหน้ากลุ่มชาวไร่อ้อยหัวหน้าโควตา",

    "องค์กรชาวไร่อ้อย": "องค์กรและสถาบันชาวไร่อ้อยและโรงงานน้ำตาล",
    "สถาบันชาวไร่อ้อย": "องค์กรและสถาบันชาวไร่อ้อยและโรงงานน้ำตาล",

    "พันธุ์อ้อยแนะนำ": "พันธุ์อ้อยที่สำนักงานคณะกรรมการอ้อยและน้ำตาลทรายแนะนำ",
    "อ้อยพันธุ์ไหนดี": "พันธุ์อ้อยที่สำนักงานคณะกรรมการอ้อยและน้ำตาลทรายแนะนำ",
    }

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
    welcome_message = f" {profile.display_name} สวัสดี คุณ {profile.display_name}\nขอบคุณที่เป็นเพื่อนกับเรา\n \nแนะนำวิธีการใช้งาน How to plant Aoi\n\nเเชทบอทตอบคำถามเกี่ยวกับอ้อย\n\nราคาอ้อย\nพรบ.อ้อย\nอุณหภูมิ\nc.c.s\n\nลองพิมพ์คำว่า c.c.s"
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_message)
    )
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message in image_map_keys:
        image_key = image_map_keys[user_message]
        image_url = image_map.get(image_key)
    
        if image_url:
            image_message = ImageSendMessage(
                original_content_url=image_url,
                preview_image_url=image_url
            )
            line_bot_api.reply_message(
                event.reply_token,
                image_message
            )
    elif user_message in ["ราคาอ้อย", "ราคาอ้อยตันละเท่าไหร่", "ราคาอ้อยวันนี้", "price"]:
        text = "ราคาเฉลี่ยทั่วประเทศในอัตราที่ 1,197.53 บาท/ตัน ณ ระดับความหวานที่ 10 ซี.ซี.เอส. กำหนดอัตราขึ้น/ลงของราคาอ้อย เท่ากับ 71.85 บาทต่อ 1 หน่วย ซี.ซี.เอส. และผลตอบแทนการผลิตและจำหน่ายน้ำตาลทราย 513.23 บาท/ตัน"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif user_message in ["act", "พรบอ้อยเเละน้ำตาล", "พรบอ้อย", "พระราชบัญญัติอ้อยและน้ำตาล","พรบ.อ้อย"]:
        text = "https://www.ratchakitcha.soc.go.th/DATA/PDF/2565/A/078/T_0001.PDF"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    elif user_message in ["details", "detail", "รายละเอียด","รายละเอียดของอ้อย","รายละเอียดอ้อย"]:
        # Define a Flex Message for details
        carousel_flex_message = {
            "type": "carousel",
            "contents": [
                {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://drive.google.com/uc?id=11DMMadUwTNlS66wKW6DzYhtt4jhStSBn",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์เบา",
                        "weight": "bold",
                        "size": "xl"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์เบา \nคืออ้อยที่มีการสะสมน้ำตาลเร็วและมีอายุเก็บเกี่ยวประมาณ 8-10 เดือน ซึ่งอาจเก็บเกี่ยวได้ในช่วงเดือนพฤศจิกายน – ธันวาคม",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "action": {
                            "type": "uri",
                            "label": "รายละเอียดเพิ่มเติม",
                             "uri": "https://www.mitrpholmodernfarm.com/news/2020/08/%E0%B8%9E%E0%B8%B1%E0%B8%99%E0%B8%98%E0%B8%B8%E0%B9%8C%E0%B8%AD%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%AB%E0%B8%A1%E0%B8%B2%E0%B8%B0%E0%B8%AA%E0%B8%A1%E0%B9%83%E0%B8%99%E0%B9%81%E0%B8%95%E0%B9%88%E0%B8%A5%E0%B8%B0%E0%B8%9E%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://drive.google.com/uc?id=1AOMWk25TYeF4-NDQvE3cFEerZ06csjCy",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์กลาง",
                        "weight": "bold",
                        "size": "xl"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์กลาง \nคืออ้อยที่มีการสะสมน้ำตาลเร็วปานกลาง อายุการเก็บเกี่ยวระหว่าง 10-12 เดือน เหมาะสำหรับการเก็บเกี่ยวช่วงเดือนมกราคม – กุมภาพันธ์",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "action": {
                            "type": "uri",
                            "label": "รายละเอียดเพิ่มเติม",
                             "uri": "https://www.mitrpholmodernfarm.com/news/2020/08/%E0%B8%9E%E0%B8%B1%E0%B8%99%E0%B8%98%E0%B8%B8%E0%B9%8C%E0%B8%AD%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%AB%E0%B8%A1%E0%B8%B2%E0%B8%B0%E0%B8%AA%E0%B8%A1%E0%B9%83%E0%B8%99%E0%B9%81%E0%B8%95%E0%B9%88%E0%B8%A5%E0%B8%B0%E0%B8%9E%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88"
                        }
                    }
                ]
            }
        },
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://drive.google.com/uc?id=1mo2Kh-lU7QnS5cLuI6NL8DlzEH43UPDY",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover"
            },
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์หนัก",
                        "weight": "bold",
                        "size": "xl"
                    }
                ]
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "อ้อยพันธุ์หนัก \nคืออ้อยที่มีการสะสมน้ำตาลช้า อายุการเก็บเกี่ยวมากกว่า 12 เดือน เหมาะสำหรับการเก็บเกี่ยวช่วงปลายฤดู",
                        "wrap": True,
                        "margin": "md"
                    },
                    {
                        "type": "separator",
                        "margin": "lg"
                    },
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "button",
                        "style": "link",
                        "action": {
                            "type": "uri",
                            "label": "รายละเอียดเพิ่มเติม",
                             "uri": "https://www.mitrpholmodernfarm.com/news/2020/08/%E0%B8%9E%E0%B8%B1%E0%B8%99%E0%B8%98%E0%B8%B8%E0%B9%8C%E0%B8%AD%E0%B9%89%E0%B8%AD%E0%B8%A2%E0%B8%97%E0%B8%B5%E0%B9%88%E0%B9%80%E0%B8%AB%E0%B8%A1%E0%B8%B2%E0%B8%B0%E0%B8%AA%E0%B8%A1%E0%B9%83%E0%B8%99%E0%B9%81%E0%B8%95%E0%B9%88%E0%B8%A5%E0%B8%B0%E0%B8%9E%E0%B8%B7%E0%B9%89%E0%B8%99%E0%B8%97%E0%B8%B5%E0%B9%88"
                        }
                    }
                ]
            }
        }
        ]
        }          
        flex_message = FlexSendMessage(alt_text="Details in Carousel", contents=carousel_flex_message)
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )
    elif user_message in ["weather", "อุณหภูมิ", "ความชื้น", "สภาพอากาศ", "อุณหภูมิในขอนเเก่น","รายงานสภาพอากาศ"]:
        weather_data = requests.get(BASE_URL).json()
        
        if weather_data['cod'] != '404':
            main_data = weather_data['main']
            temperature = main_data['temp']
            humidity = main_data['humidity']
            weather_description = weather_data['weather'][0]['description']
            
            weather_message = f"อุณภูมิ: {temperature}°C\nความชื้น: {humidity}%\nสภาพอากาศ: {weather_description}"
            
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=weather_message)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="City not found.")
            )
    else:
        try:
            response = model.generate_content(user_message + "\n ตอบเป็นภาษาไทย")
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
