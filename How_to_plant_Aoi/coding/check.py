import os
import requests

def upload_image_to_imgur(image_path):
    IMGUR_CLIENT_ID = 'YOUR_IMGUR_CLIENT_ID'  # Replace with your actual Imgur Client ID
    headers = {'Authorization': f'Client-ID {IMGUR_CLIENT_ID}'}
    
    # Check if the file exists
    if not os.path.exists(image_path):
        print("File does not exist.")
        return None

    # Upload the image
    with open(image_path, 'rb') as img:
        response = requests.post(
            'https://api.imgur.com/3/upload',
            headers=headers,
            files={'image': img}
        )

    # Handle the response
    if response.status_code == 200:
        print("Upload successful.")
        return response.json()['data']['link']
    else:
        print(f"Failed to upload. Status code: {response.status_code}")
        print("Response content:", response.json())
        return None

# Test the upload function
image_path = r'C:\Users\patth\OneDrive\Desktop\webapp\How_to_plant_Aoi\coding\1.png'
image_url = upload_image_to_imgur(image_path)

if image_url:
    print(f"Uploaded image URL: {image_url}")
else:
    print("Image upload failed.")
