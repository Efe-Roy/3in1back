import boto3
import os

# DigitalOcean Space details
AWS_ACCESS_KEY_ID = 'DO00PRT6ALVZRZ9YPQ8K'
AWS_SECRET_ACCESS_KEY = 'hlzEl2qyXWgINQuvEncA0HRri0gNZLblj+WqVZ8KNqw'
AWS_STORAGE_BUCKET_NAME = 'three-in-one-space-bucket'
AWS_S3_ENDPOINT_URL = 'https://sfo3.digitaloceanspaces.com'

# Local directory to save files
# LOCAL_DIRECTORY = 'D:\\DO_Space'
LOCAL_DIRECTORY = 'C:\\Users\\DELL\\Desktop\\procesosadministrativos'

# Initialize boto3 client
s3 = boto3.client('s3', endpoint_url=AWS_S3_ENDPOINT_URL,
                  aws_access_key_id=AWS_ACCESS_KEY_ID,
                  aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

def download_files_from_space(space_folder=''):
    # List all objects in the space folder
    response = s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=space_folder)

    # Check if there are any objects
    if 'Contents' in response:
        objects = response['Contents']

        # Download each object
        for obj in objects:
            key = obj['Key']
            if key.endswith('/'):
                # It's a folder, create local folder and recursively download its content
                folder_name = key.rstrip('/')
                next_space_folder = os.path.join(space_folder, folder_name)
                download_files_from_space(next_space_folder)
            else:
                # It's a file, download it
                local_file_path = os.path.join(LOCAL_DIRECTORY, key)
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)  # Create parent directory if not exists
                print(f"Downloading {key}...")
                s3.download_file(AWS_STORAGE_BUCKET_NAME, key, local_file_path)
                print(f"Downloaded {key} to {local_file_path}")
    else:
        print(f"No objects found in folder: {space_folder}")

if __name__ == "__main__":
    download_files_from_space()