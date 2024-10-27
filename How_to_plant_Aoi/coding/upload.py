from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageSendMessage

app = Flask(__name__)

# LINE Bot configuration
LINE_CHANNEL_ACCESS_TOKEN = '49OWRVMFEPUphOLl3iNBWbBnA25oonIMuu3Gjl4wlzgsdwrxXwOgYfQ8MJIkreoNVr6iDIFvBWfOerCXllSKLCvu3SO8b9aGFfirxF+H/eaYJa3La8AV6nW3osSTkrzV93xWE+QiOuWVTGoC6oM/BwdB04t89/1O/w1cDnyilFU='
LINE_CHANNEL_SECRET = 'b8ca496d4f97dede39ba2f519890989e'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

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

    "พรบ.อ้อยและน้ำตาล": "พระราชบัญญัติอ้อยและน้ำตาลทรายพ.ศ.2527มีเนื้อหาโดยสรุปอย่างไร",
    "พระราชบัญญัติอ้อยและน้ำตาล": "พระราชบัญญัติอ้อยและน้ำตาลทรายพ.ศ.2527มีเนื้อหาโดยสรุปอย่างไร",
    "พรบอ้อย": "พระราชบัญญัติอ้อยและน้ำตาลทรายพ.ศ.2527มีเนื้อหาโดยสรุปอย่างไร",
    "พรบอ้อยเเละน้ำตาล": "พระราชบัญญัติอ้อยและน้ำตาลทรายพ.ศ.2527มีเนื้อหาโดยสรุปอย่างไร",

    "พันธุ์อ้อยแนะนำ": "พันธุ์อ้อยที่สำนักงานคณะกรรมการอ้อยและน้ำตาลทรายแนะนำ",
    "อ้อยพันธุ์ไหนดี": "พันธุ์อ้อยที่สำนักงานคณะกรรมการอ้อยและน้ำตาลทรายแนะนำ",
    }

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
# Function to handle user messages and send corresponding image

    user_message = event.message.text.lower()

    if user_message in image_map_keys:
        image_key = image_map_keys[user_message]
        image_url = image_map.get(image_key)
    # Perform further actions with image_url
    
    if image_url:
        # Send the image using ImageSendMessage
        image_message = ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        )
        line_bot_api.reply_message(
            event.reply_token,
            image_message
        )


if __name__ == "__main__":
    app.run(port=5000, debug=True)

