from dataclasses import dataclass
from typing import Union

from hikari import Snowflake

from bot.clients.table_client import DataConnection

USER_PARTITION_KEY = "user"
SCORE_PARTITION_KEY = "score"


@dataclass
class WordleScore:
    """A representation of a Wordle score."""

    author: str
    score: str
    number: str
    hard_mode: bool
    solver: bool

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
        """Save the score to the table."""
        __class__.client.save(self.to_storage_dict())

    @staticmethod
    def from_storage_table(row) -> "WordleScore":
        """Convert from a storage table row."""
        return WordleScore(
            author=row["author"],
            score=row["score"],
            number=row["number"],
            hard_mode=row["hard_mode"],
            solver=row["solver"],
        )

    @staticmethod
    def query(query: str):
        """Query the table."""
        return __class__.client.query(WordleScore.from_storage_table, query)

    @classmethod
    def query_by_number(cls, number: Union[str, int]):
        """Query all scores by number."""
        query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{number}'"
        return cls.query(query)

    @classmethod
    def query_by_author(cls, author: Union[str, Snowflake]):
        """Query all scores by number."""
        query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{author}'"
        return cls.query(query)

    def to_storage_dict(self):
        """Convert to a dict."""
        return {
            "PartitionKey": SCORE_PARTITION_KEY,
            "RowKey": f"{self.author}-{self.number}",
            "author": self.author,
            "score": self.score,
            "number": self.number,
            "hard_mode": self.hard_mode,
            "solver": self.solver,
        }


conn = DataConnection("wordle")
WordleScore.client = conn
