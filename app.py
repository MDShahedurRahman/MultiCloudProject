import base64
import html
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import boto3
import json
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
import cv2
import numpy as np
import urllib.request
from datetime import datetime
from urllib.parse import quote_plus, unquote_plus
from image_processing import process_image
from image_saving import save_to_firestore
from image_displaying import get_image_data_from_firestore
from google.cloud import firestore

from image_uploading import upload_image_to_s3

app = Flask(__name__)

# Set a secret key for the application
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Initialize AWS SDK
s3 = boto3.client('s3')

# Initialize Firestore client
db = firestore.Client.from_service_account_json('./multicloudproject-420507-9400a3d3205a.json')

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/cloudidentify', methods=['GET', 'POST'])
def home():
    return render_template('index.html')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():  
    return render_template('login.html')


@app.route('/upload', methods=['POST'])
def upload_photo():
    data = request.json
    filename = data['filename']
    image_data = base64.b64decode(data['image'])

    # Upload image to S3 and get the presigned URL
    presigned_url = upload_image_to_s3(image_data, filename)

    if presigned_url:
        # Process the image using the Azure Computer Vision API
        if process_image(presigned_url, session):
            return redirect(url_for('process_result'))
        else:
            return 'Error processing image'
    else:
        return 'Error uploading image'


@app.route('/upload-file', methods=['POST'])
def upload_file():
    print("Received file upload request")  # Debug log
    if 'image' in request.files:
        try:
            image = request.files['image']
            filename = image.filename
            image_data = image.read()

            # Upload image to S3 and get the presigned URL
            presigned_url = upload_image_to_s3(image_data, filename)

            if presigned_url:
                # Process the image using the Azure Computer Vision API
                if process_image(presigned_url, session):
                    return redirect(url_for('process_result'))
                else:
                    return 'Error processing image'
            else:
                return 'Error uploading image'
        except Exception as e:
            print(f'Error uploading image: {str(e)}')  # Debug log
            return f'Error uploading image: {str(e)}'
    else:
        print("No image received")  # Debug log
        return 'No image received'
    
@app.route('/process-result', methods=['GET', 'POST'])
def process_result():
    # Retrieve data from session
    imageDescription = session.get('image_description', '')
    dateTime = session.get('date_time', '')
    imageLink = session.get('image_link', '')

    # Render result.html template with the provided data
    return render_template('result.html', 
                           image_description=imageDescription, 
                           date_time=dateTime, 
                           image_link=imageLink)

@app.route('/save-image', methods=['POST'])
def save_image_to_firestore():
    data = request.json
    image_url = data.get('image_url')
    image_description = data.get('image_description')
    date_time = data.get('date_time')
    image_link = data.get('image_link')

    # Call the function to save image data to Firestore
    save_to_firestore(image_url, image_description, date_time, image_link)

    return 'Image data saved successfully!', 200

@app.route('/album')
def display_images():
    # Get image data from Firestore using the function from image_displaying.py
    image_data = get_image_data_from_firestore(db)

    # Render HTML template with sorted data
    return render_template('images.html', images=image_data)

@app.route('/favicon.ico')
def favicon():
    return '', 204


if __name__ == '__main__':
    app.run(debug=True)