from google.cloud import firestore
import html

def get_image_data_from_firestore(db):
    # Query Firestore to retrieve image data
    images_ref = db.collection('images')
    images = images_ref.get()

    # Prepare data to pass to template
    image_data = []
    for image in images:
        image_dict = image.to_dict()
        # Decode HTML entities in image link
        image_dict['ImageLink'] = html.unescape(image_dict['ImageLink'])
        image_dict['Image'] = html.unescape(image_dict['Image'])
        image_data.append(image_dict)

    # Sort the image data by 'DateAndTime' in descending order
    image_data.sort(key=lambda x: x['DateAndTime'], reverse=True)
    return image_data
