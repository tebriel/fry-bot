from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.keyvault.secrets import SecretClient
from azure.search.documents import SearchClient

ENDPOINT = 'https://haiku-search-service.search.windows.net'

credential = DefaultAzureCredential()
secret_client = SecretClient('https://fry-bot.vault.azure.net/', credential)
search_key = secret_client.get_secret('api-search-key')

def connect(index: str) -> SearchClient:
    """connect to the search service."""
    return SearchClient(
        endpoint=ENDPOINT,
        index_name=index,
        credential=AzureKeyCredential(search_key.value))
