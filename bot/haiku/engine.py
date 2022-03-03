import random
from typing import List

from bot.haiku.models import FormedHaiku, HaikuKey, HaikuLine, HaikuMetadata
from bot.haiku.search import HaikuSearch


class Haiku:
    """Yet another Haiku Engine."""

    def add_line(self, size: HaikuKey, text: str, author: str = "") -> FormedHaiku:
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

    @classmethod
    def make_haiku(cls, seed_entity: HaikuLine = None) -> FormedHaiku:
        """
        Make a haiku.

        todo: Use HaikuLines instead of strings
        """
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

        entity = FormedHaiku(poem=lines)
        entity.save()
        return entity

    @classmethod
    def about(cls, term: str = None) -> FormedHaiku:
        """Make a haiku about a term."""
        if term is None:
            term = ""
        searches = HaikuSearch.search(term=term)
        if not searches:
            return f"I don't know about {term}"

        entity = random.choice(searches)
        return cls.make_haiku(seed_entity=entity)
