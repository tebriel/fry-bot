import json
import random
from datetime import datetime
from typing import List

from bot.clients.search_client import connect as search_connect
from bot.haiku.model import HaikuKey, HaikuLine, HaikuMetadata


class Haiku:
    """Yet another Haiku Engine."""

    _search_clients = None

    def _get_search_clients(self):
        if self._search_clients is None:
            self._search_clients = [
                search_connect("haiku-fives-index"),
                search_connect("haiku-sevens-index"),
            ]
        return self._search_clients

    search_clients = property(_get_search_clients)

    def add_line(self, size: HaikuKey, text: str, author: str = "") -> str:
        """Adds a line."""

        entity = HaikuLine(
            line=text,
            size=size,
            author=author,
        )
        entity.save()
        return self.make_haiku(seed_entity=entity)

    def random_line(self, size: HaikuKey) -> str:
        """Get a random line."""
        metadata = HaikuMetadata.get(size=size)
        max_id = metadata.max_id
        if max_id <= 0:
            return "no data found"
        row_key = random.randint(0, max_id)
        entity = self.client.get_entity(partition_key=str(size), row_key=str(row_key))
        return entity["Line"]

    def store_haiku(self, lines: List[str], c_date: str = None) -> None:
        """Store a haiku."""
        if c_date is None:
            c_date = datetime.utcnow().isoformat()
        entity = {
            "PartitionKey": str(HaikuKey.FORMED),
            "RowKey": c_date,
            "Poem": json.dumps(lines),
        }
        self.client.upsert_entity(entity=entity)

    def make_haiku(self, seed_entity: HaikuLine = None) -> str:
        """Make a haiku."""
        lines = []
        lines.append(self.random_line(HaikuKey.FIVE))
        lines.append(self.random_line(HaikuKey.SEVEN))
        lines.append(self.random_line(HaikuKey.FIVE))
        if seed_entity is not None:
            if seed_entity.size == HaikuKey.FIVE:
                lines[random.choice([0, 2])] = seed_entity.line
            else:
                lines[1] = seed_entity.line
        self.store_haiku(lines)
        return "\n".join(lines)

    def about(self, term: str = None) -> str:
        """Make a haiku about a term."""
        searches = []
        for result in [x.search(term) for x in self.search_clients]:
            searches += list(result)
        if not searches:
            return f'I don\'t know about "{term}"'

        entity = random.choice(searches)
        return self.make_haiku(seed_entity=entity)
