from dataclasses import dataclass
from enum import Enum

from bot.clients.table_client import DataConnection

USER_PARTITION_KEY = "user"
SCORE_PARTITION_KEY = "score"


class HaikuKey(Enum):
    """Partition keys for the haiku table."""

    FIVE = "FIVE"
    SEVEN = "SEVEN"
    FORMED = "FORMED"


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
        if row["PartitionKey"].endswith("FIVE"):
            size = HaikuKey.FIVE
        else:
            size = HaikuKey.SEVEN
        print(row)
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

    def to_storage_dict(self):
        """Convert to a dict."""
        return {
            "PartitionKey": str(self.size),
            "RowKey": str(self.id_),
            "Author": self.author,
            "Line": self.line,
        }


conn = DataConnection("haiku")
HaikuMetadata.client = conn
HaikuLine.client = conn
