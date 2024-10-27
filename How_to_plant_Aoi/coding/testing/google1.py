import requests
import json

def send_image_message(original_url, preview_url):
    # Construct the payload
    payload = {
        "type": "image",
        "originalContentUrl": original_url,
        "previewImageUrl": preview_url
    }

    # Convert payload to JSON
    json_payload = json.dumps(payload)

    # Set up the headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer YOUR_ACCESS_TOKEN_HERE'  # Replace with your actual access token
    }

    # URL to send the request to (replace with the actual API endpoint)
    url = 'https://api.example.com/send_image'

    # Send the POST request
    response = requests.post(url, data=json_payload, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Image message sent successfully!")
    else:
        print(f"Failed to send image message. Status code: {response.status_code}")
        print(f"Response: {response.text}")

# Example usage
original_image_url = "https://example.com/original.jpg"
preview_image_url = "https://example.com/preview.jpg"

send_image_message(original_image_url, preview_image_url)