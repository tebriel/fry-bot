import os

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__

client: BlobServiceClient = None
container = "fry-bot-haiku"
connect_str = os.getenv('AZURE_STORAGE_CONNECTION_STRING')

FIVE = 'five'
SEVEN = 'seven'

def connect() -> BlobServiceClient:
    global client
    if client != None:
        return client
    client = BlobServiceClient.from_connection_string(connect_str)
    return client

def add_line(size: str, text: str) -> str:
    client = connect().get_blob_client(container, str(size))
    if client.exists():
        text = client.download_blob().readall().decode()
        client.delete_blob()
    


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