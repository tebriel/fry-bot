from typing import Any, Callable, Generator, Optional, TypeVar

from azure.data.tables import TableClient, TableServiceClient
from azure.identity import DefaultAzureCredential

ModelType = TypeVar("ModelType")


def table_client() -> TableServiceClient:
    """connect to the table service."""
    credential = DefaultAzureCredential()
    client = TableServiceClient(
        endpoint="https://frybot.table.core.windows.net/", credential=credential
    )
    return client


def connect(table: str) -> TableClient:
    """connect to the table service."""
    conn = table_client()
    return conn.get_table_client(table_name=table)


class DataConnection:
    """Manage a connection to the StorageTable."""

    _table_client: Optional[TableClient] = None

    def __init__(self, client: TableClient = None):
        if client is not None:
            self._table_client = client

    @property
    def table_client(self) -> TableClient:
        """Gets the table client."""
        if self._table_client is None:
            self._table_client = connect("wordle")
        return self._table_client

    def save(self, entity: dict[str, Any]):
        """Save an entity."""
        self.table_client.upsert_entity(entity=entity)

    def query(
        self, hydrator: Callable[[dict], ModelType], query: str
    ) -> Generator[ModelType, None, None]:
        """Query the table."""
        for result in self.table_client.query_entities(query):
            yield hydrator(result)
