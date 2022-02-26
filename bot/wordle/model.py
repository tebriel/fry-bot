from dataclasses import dataclass
from typing import Union

from hikari import Snowflake

from bot.clients.table_client import DataConnection

USER_PARTITION_KEY = "user"
SCORE_PARTITION_KEY = "score"

conn = DataConnection("wordle")


@dataclass
class WordleScore:
    """A representation of a Wordle score."""

    author: str
    score: str
    number: str
    hard_mode: bool
    solver: bool

    def save(self, data_client: DataConnection = None) -> None:
        """Save the score to the table."""
        if data_client is None:
            data_client = conn
        data_client.save(self.to_storage_dict())

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
    def query(query: str, data_client: DataConnection = None):
        """Query the table."""
        if data_client is None:
            data_client = conn
        return data_client.query(WordleScore.from_storage_table, query)

    @classmethod
    def query_by_number(
        cls, number: Union[str, int], data_client: DataConnection = None
    ):
        """Query all scores by number."""
        query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{number}'"
        return cls.query(query, data_client)

    @classmethod
    def query_by_author(
        cls, author: Union[str, Snowflake], data_client: DataConnection = None
    ):
        """Query all scores by number."""
        query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{author}'"
        return cls.query(query, data_client)

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
