from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace with your LINE channel access token
LINE_CHANNEL_ACCESS_TOKEN = '2d2aceb6784907982259211844276aa2'

@app.route("/callback", methods=['POST'])
def callback():
    body = request.get_json()

    # Check if 'events' exists and is not empty

    event = body['events'][0]

        # Check if the message type is 'location'

            # Get latitude and longitude
    latitude = event['message']['latitude']
    longitude = event['message']['longitude']
            
            # Process the location data
    print(f"User's location: {latitude}, {longitude}")
            
            # Respond back to the user with their location
    user_id = event['source']['userId']
    reply_token = event['replyToken']
    reply_message = f"Your location: {latitude}, {longitude}"

    send_reply(reply_token, reply_message)


    return "OK"

def send_reply(reply_token, message):
    url = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_CHANNEL_ACCESS_TOKEN}'
    }
    data = {
        'replyToken': reply_token,
        'messages': [{
            'type': 'text',
            'text': message
        }]
    }
    requests.post(url, headers=headers, json=data)

if __name__ == "__main__":
    app.run(debug=True)
