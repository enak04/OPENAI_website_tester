from azure.storage.blob import BlobServiceClient

blob_conn_str = "<your-blob-connection-string>"
container_name = "users"

blob_service_client = BlobServiceClient.from_connection_string(blob_conn_str)
container_client = blob_service_client.get_container_client(container_name)

def upload_user_file(user_id, file_name, content):
    blob_path = f"{user_id}/{file_name}"  # e.g., anirudh123/theme.css
    blob_client = container_client.get_blob_client(blob_path)
    blob_client.upload_blob(content, overwrite=True)
