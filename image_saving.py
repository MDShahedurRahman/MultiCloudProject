from google.cloud import firestore
import datetime

# Initialize Firestore client
db = firestore.Client.from_service_account_json('./multicloudproject-420507-9400a3d3205a.json')

# Function to save data to Firestore
def save_to_firestore(image_url, image_description, date_time, image_link):
    # Define data to be saved
    data = {
        'Image': image_url,
        'ImageDescription': image_description,
        'DateAndTime': date_time,
        'ImageLink' : image_link
    }
    
    # Add data to Firestore
    doc_ref = db.collection('images').add(data)
    doc_id = doc_ref[1].id  # Accessing the document ID
    print(f'Document added with ID: {doc_id}')

# Usage example
if __name__ == '__main__':
    # Sample data
    image_url = 'https://example.com/image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVRUVWPJ2M2KLWPNB%2F20240416%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240416T000000Z&X-Amz-Expires=86400&X-Amz-Signature=c3dcdf2f0332460ce2cf1b2fee9bc2a60c3eacd48a8480bd0dce1197178325fa&X-Amz-SignedHeaders=host'
    image_description = 'A beautiful landscape'
    date_time = datetime.datetime.now()
    image_link = 'https://example.com/image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVRUVWPJ2M2KLWPNB%2F20240416%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20240416T000000Z&X-Amz-Expires=86400&X-Amz-Signature=c3dcdf2f0332460ce2cf1b2fee9bc2a60c3eacd48a8480bd0dce1197178325fa&X-Amz-SignedHeaders=host'

    # Save data to Firestore
    save_to_firestore(image_url, image_description, date_time, image_link)

