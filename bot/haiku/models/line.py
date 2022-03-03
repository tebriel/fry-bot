from dataclasses import dataclass
from typing import Optional, TypedDict

from bot.clients.table_client import DataConnection

from .key import HaikuKey
from .metadata import HaikuMetadata


class LineStorageFormat(TypedDict):
    """Data representation of a line."""

    PartitionKey: HaikuKey
    RowKey: str
    Author: str
    Line: str


@dataclass
class HaikuLine:
    """A representation of a Wordle score."""

    size: HaikuKey
    id_: str
    line: str
    author: str

    def __init__(self, **kwargs):
        """Initialize the Haiku Line."""
        self.id_ = kwargs.get("id_", None)
        self.size = kwargs.get("size", HaikuKey.FIVE)
        self.line = kwargs.get("line", "")
        self.author = kwargs.get("author", "")

    @property
    @classmethod
    def client(cls) -> DataConnection:
        """Get the data client."""
        return getattr(cls, "__client", None)

    @client.setter
    @classmethod
    def client(cls, client: DataConnection):
        """Set the data client."""
        setattr(cls, "__client", client)

    def save(self) -> None:
        """Save the model to the table."""
        if self.id_ is None:
            metadata = HaikuMetadata.get(self.size)
            self.id_ = metadata.increment_id()
        __class__.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "HaikuLine":
        """Convert from a storage table row."""
        size = HaikuKey(row["PartitionKey"])
        return HaikuLine(
            size=size,
            id_=int(row["RowKey"]),
            author=row.get("author", ""),
            line=row["Line"],
        )

    @staticmethod
    def query(query: str):
        """Query the table."""
        return __class__.client.query(HaikuLine.from_storage_table, query)

    @classmethod
    def get(cls, size: HaikuKey, id_: int) -> Optional["HaikuLine"]:
        """Get the metadata for a given size."""
        entity = cls.client.get(
            partition_key=size.value,
            row_key=str(id_),
            hydrator=cls.from_storage_table,
        )
        return entity

    def to_storage_dict(self) -> LineStorageFormat:
        """Convert to a dict."""
        return {
            "PartitionKey": self.size.value,
            "RowKey": str(self.id_),
            "Author": self.author,
            "Line": self.line,
        }
