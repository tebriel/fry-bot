from dataclasses import dataclass
from http.client import NotConnected
from typing import TypedDict

from bot.clients.table_client import DataConnection

from .key import HaikuKey


class MetdataStorageFormat(TypedDict):
    """Data representation of a line."""

    PartitionKey: str
    RowKey: str
    MaxID: int


@dataclass
class HaikuMetadata:
    """A representation of a Wordle score."""

    size: HaikuKey
    max_id: int

    ROW_KEY = "METADATA"

    @property
    @staticmethod
    def client() -> DataConnection:
        """Get the data client."""
        result = getattr(HaikuMetadata, "__client", None)
        if result is None:
            raise NotConnected("No client available")
        return result

    @client.setter
    @staticmethod
    def client(client: DataConnection):
        """Set the data client."""
        setattr(HaikuMetadata, "__client", client)

    @staticmethod
    def get(size: HaikuKey) -> "HaikuMetadata":
        """Get the metadata for a given size."""
        entity = HaikuMetadata.client.get(
            partition_key=size.value,
            row_key=HaikuMetadata.ROW_KEY,
            hydrator=HaikuMetadata.from_storage_table,
        )
        if entity is None:
            entity = HaikuMetadata(size=size, max_id=0)
        return entity

    def save(self) -> None:
        """Save the model to the table."""
        HaikuMetadata.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "HaikuMetadata":
        """Convert from a storage table row."""
        size = HaikuKey(row["PartitionKey"])
        return HaikuMetadata(
            size=size,
            max_id=int(row.get("MaxID", 0)),
        )

    def to_storage_dict(self) -> MetdataStorageFormat:
        """Convert to a dict."""
        return {
            "PartitionKey": self.size.value,
            "RowKey": self.ROW_KEY,
            "MaxID": self.max_id,
        }

    def increment_id(self) -> int:
        """Increment the ID."""
        self.max_id += 1
        self.save()
        return self.max_id
