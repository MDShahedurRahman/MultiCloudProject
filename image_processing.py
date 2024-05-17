import json
from datetime import datetime
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
import boto3

def process_image(image_url, session):
    try:
        # Access Azure Computer Vision API
        vision_credential = json.load(open('visioncredential.json'))
        API_KEY = vision_credential['API_KEY']
        ENDPOINT = vision_credential['ENDPOINT']

        computervision_client = ComputerVisionClient(ENDPOINT, CognitiveServicesCredentials(API_KEY))

        # Call the Azure Cognitive Services Vision API to describe the image
        description_result = computervision_client.describe_image(image_url)

        # Extract the descriptions from the result
        descriptions = [caption.text for caption in description_result.captions]

        # Store the data in session
        session['image_description'] = descriptions[0]
        session['date_time'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session['image_link'] = image_url

        return True
    except Exception as e:
        print(f'Error processing image: {str(e)}')  # Debug log
        return False
