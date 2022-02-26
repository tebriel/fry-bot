import random
from typing import List

from bot.clients.search_client import connect as search_connect
from bot.haiku.models import FormedHaiku, HaikuKey, HaikuLine, HaikuMetadata


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

    @staticmethod
    def random_line(size: HaikuKey) -> str:
        """Get a random line."""
        metadata = HaikuMetadata.get(size=size)
        max_id = metadata.max_id
        if max_id <= 0:
            return "no data found"
        row_key = random.randint(0, max_id)
        entity = HaikuLine.get(size=size, id_=row_key)
        if entity is None:
            return "line not found in store"
        return entity.line

    @staticmethod
    def store_haiku(lines: List[str], c_date: str = None) -> None:
        """Store a haiku."""
        entity = FormedHaiku(
            created_at=c_date,
            poem=lines,
        )
        entity.save()

    def make_haiku(self, seed_entity: HaikuLine = None) -> str:
        """Make a haiku."""
        lines: List[str] = [
            self.random_line(HaikuKey.FIVE),
            self.random_line(HaikuKey.SEVEN),
            self.random_line(HaikuKey.FIVE),
        ]
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
