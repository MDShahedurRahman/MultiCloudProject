import boto3

# Initialize AWS SDK
s3 = boto3.client('s3')

def upload_image_to_s3(image_data, filename):
    try:
        # Upload image to S3 with the original filename
        s3.put_object(Bucket='imagestoragee8ab2-dev', Key=filename, Body=image_data)
        # Generate a pre-signed URL for the uploaded image
        presigned_url = s3.generate_presigned_url(
            'get_object',
            Params={'Bucket': 'imagestoragee8ab2-dev', 'Key': filename},
            ExpiresIn=604800
        )
        return presigned_url
    except Exception as e:
        print(f'Error uploading image: {str(e)}')  # Debug log
        return None
