from dataclasses import dataclass

from bot.clients.table_client import DataConnection

from .key import HaikuKey


@dataclass
class HaikuMetadata:
    """A representation of a Wordle score."""

    size: HaikuKey
    max_id: int

    ROW_KEY = "METADATA"

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
    def get(cls, size: HaikuKey) -> "HaikuMetadata":
        """Get the metadata for a given size."""
        entity = cls.client.get(
            partition_key=str(size),
            row_key=cls.ROW_KEY,
            hydrator=cls.from_storage_table,
        )
        if entity is None:
            entity = HaikuMetadata(size=size, max_id=0)
        return entity

    def save(self) -> None:
        """Save the model to the table."""
        __class__.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "HaikuMetadata":
        """Convert from a storage table row."""
        if row["PartitionKey"].endswith("FIVE"):
            size = HaikuKey.FIVE
        else:
            size = HaikuKey.SEVEN
        return HaikuMetadata(
            size=size,
            max_id=int(row.get("max_id", 0)),
        )

    def to_storage_dict(self):
        """Convert to a dict."""
        return {
            "PartitionKey": str(self.size),
            "RowKey": self.ROW_KEY,
            "max_id": self.max_id,
        }

    def increment_id(self) -> int:
        """Increment the ID."""
        self.max_id += 1
        self.save()
        return self.max_id
