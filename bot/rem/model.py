from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Union

from hikari import Snowflake

from bot.clients.table_client import DataConnection

PARTITION_KEY = "fact"


@dataclass
class Fact:
    """A representation of a Wordle score."""

    author: str
    name: str
    fact: str
    created_at: datetime

    def __init__(self, **args):
        self.author = args.get("author", "")
        self.name = args.get("name", "")
        self.fact = args.get("fact", "")
        self.created_at = args.get("created_at", datetime.utcnow())

    @property
    @classmethod
    def client(cls) -> Optional[DataConnection]:
        """Get the data client."""
        return getattr(cls, "__client", None)

    @client.setter
    @classmethod
    def client(cls, client: DataConnection):
        """Set the data client."""
        setattr(cls, "__client", client)

    def save(self) -> None:
        """Save the score to the table."""
        __class__.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "Fact":
        """Convert from a storage table row."""
        return Fact(
            author=row["Author"],
            name=row["RowKey"],
            fact=row["Fact"],
            created_at=datetime.fromisoformat(row["CreatedAt"]),
        )

    @staticmethod
    def query(query: str):
        """Query the table."""
        return __class__.client.query(Fact.from_storage_table, query)

    @classmethod
    def query_by_name(cls, name: str):
        """Query all facts by name."""
        query = f"PartitionKey eq '{PARTITION_KEY}' and RowKey eq '{name}'"
        return cls.query(query)

    @classmethod
    def query_by_author(cls, author: Union[str, Snowflake]):
        """Query all scores by number."""
        query = f"PartitionKey eq '{PARTITION_KEY}' and Author eq '{author}'"
        return cls.query(query)

    def to_storage_dict(self):
        """Convert to a dict."""
        return {
            "PartitionKey": PARTITION_KEY,
            "RowKey": self.name,
            "Author": self.author,
            "Fact": self.fact,
            "CreatedAt": self.created_at.isoformat(),
        }


conn = DataConnection("rem")
Fact.client = conn
