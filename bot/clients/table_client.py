from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient, TableClient

def table_client() -> TableServiceClient:
    """connect to the table service."""
    credential = DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True)
    client = TableServiceClient(
        endpoint="https://frybot.table.core.windows.net/",
        credential=credential
    )
    return client


def connect(table: str) -> TableClient:
    """connect to the table service."""
    conn = table_client()
    return conn.get_table_client(table_name=table)
