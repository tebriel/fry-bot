import json
from dataclasses import dataclass
from datetime import datetime
from typing import List

from bot.clients.table_client import DataConnection

from .key import HaikuKey


@dataclass
class FormedHaiku:
    """A fully formed Haiku."""

    created_at: datetime
    poem: List[str]

    def __init__(self, **kwargs):
        """Initialize the model."""
        self.created_at = kwargs.get("created_at") or datetime.utcnow()
        self.poem = kwargs["poem"]

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

    @classmethod
    def get(cls, created_at: datetime) -> "FormedHaiku":
        """Get the metadata for a given size."""
        entity = cls.client.get(
            partition_key=HaikuKey.FORMED.value,
            row_key=created_at.isoformat(),
            hydrator=cls.from_storage_table,
        )
        return entity

    def save(self) -> None:
        """Save the model to the table."""
        __class__.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "FormedHaiku":
        """Convert from a storage table row."""
        return FormedHaiku(
            created_at=datetime.fromisoformat(row["RowKey"]),
            poem=json.loads(row["poem"]),
        )

    def to_storage_dict(self):
        """Convert to a dict."""
        return {
            "PartitionKey": HaikuKey.FORMED.value,
            "RowKey": self.created_at.isoformat(),
            "Poem": json.dumps(self.poem),
        }
