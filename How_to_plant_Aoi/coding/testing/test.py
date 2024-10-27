from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai
from openai import OpenAI
import os


weatherapi = '2d2aceb6784907982259211844276aa2'

app = Flask(__name__)

line_bot_api = LineBotApi('49OWRVMFEPUphOLl3iNBWbBnA25oonIMuu3Gjl4wlzgsdwrxXwOgYfQ8MJIkreoNVr6iDIFvBWfOerCXllSKLCvu3SO8b9aGFfirxF+H/eaYJa3La8AV6nW3osSTkrzV93xWE+QiOuWVTGoC6oM/BwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b8ca496d4f97dede39ba2f519890989e')

openai.api_key = os.environ.get('2a3fdff4f90d4edfab8d27af03f89601')

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    
    return 'OK'

# @handler.add(MessageEvent, message=TextMessage)
# def handle_message(event):
#     user_message = event.message.text
    
    # response = openai.ChatCompletion.create(
    #     model="gpt-4",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": user_message}
    #     ]
    # )
    
    
    
    # completion = client.chat.completions.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "You are a helpful assistant."},
    #         {"role": "user", "content": user_message}
    #     ]
    # )
    # ai_response = completion.choices[0].message.content

    # # Print the response from the assistant
    # print(completion.choices[0].message["content"]) 



    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(text=ai_response)
    # )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        ai_response = completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {str(e)}")
        ai_response = "I'm sorry, I'm having trouble processing your request right now. Please try again later."
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=ai_response)
    )


if __name__ == "__main__":
    app.run()