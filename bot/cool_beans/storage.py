import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

client: BlobServiceClient = None
container = "cool-beans"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

def connect() -> BlobServiceClient:
    global client
    if client != None:
        return client
    client = BlobServiceClient.from_connection_string(connect_str)
    return client

def increment_beans(user_id: str, count: int) -> int:
    client = connect().get_blob_client(container, str(user_id))
    if client.exists():
        beans = int(client.download_blob().readall().decode())
        client.delete_blob()
    else:
        beans = 0
    beans += count
    client.upload_blob(str(beans).encode())
    return beans