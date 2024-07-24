from google.cloud import storage
from glob import glob
import os

# Set key credentials file path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = '/home/mikee/data-lake-with-storage-bucket/mle2-lab1-91f7227387e4.json'

# Define function that uploads a file to the bucket
def upload_cs_file(bucket_name, source_file_name, destination_file_name): 
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)

    blob = bucket.blob(destination_file_name)
    blob.upload_from_filename(source_file_name)

    print(f"Uploaded {source_file_name} to {destination_file_name}")

def main():
    bucket_name = 'mle_lab1_bucket'
    source_folder = '/home/mikee/data-lake-with-storage-bucket/data/pump/'  # Đường dẫn tới thư mục chứa các file Parquet
    destination_folder = 'pump/'  # Thư mục đích trên bucket

    # Get list of all Parquet files in the source folder
    all_fps = glob(os.path.join(source_folder, "*.parquet"))

    for fp in all_fps:
        destination_blob_name = os.path.join(destination_folder, os.path.basename(fp))
        upload_cs_file(bucket_name, fp, destination_blob_name)

if __name__ == "__main__":
    main()
