import random
from typing import List

from bot.haiku.models import FormedHaiku, HaikuKey, HaikuLine, HaikuMetadata
from bot.haiku.search import HaikuSearch


class Haiku:
    """Yet another Haiku Engine."""

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

    @classmethod
    def make_haiku(cls, seed_entity: HaikuLine = None) -> str:
        """Make a haiku."""
        lines: List[str] = [
            cls.random_line(HaikuKey.FIVE),
            cls.random_line(HaikuKey.SEVEN),
            cls.random_line(HaikuKey.FIVE),
        ]
        if seed_entity is not None:
            if seed_entity.size == HaikuKey.FIVE:
                lines[random.choice([0, 2])] = seed_entity.line
            else:
                lines[1] = seed_entity.line
        cls.store_haiku(lines)
        return "\n".join(lines)

    @classmethod
    def about(cls, term: str = None) -> str:
        """Make a haiku about a term."""
        searches = HaikuSearch.search(term=term)

        entity = random.choice(searches)
        return cls.make_haiku(seed_entity=entity)
