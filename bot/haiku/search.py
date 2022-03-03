from bot.clients.search_client import SearchClient
from bot.clients.search_client import connect as search_connect
from bot.haiku.models import HaikuKey, HaikuLine


class HaikuSearch:
    """Finds HaikuLines from the database."""

    @staticmethod
    def clients() -> dict[HaikuKey, SearchClient]:
        """Initializes search clients."""
        return {
            HaikuKey.FIVE: search_connect("haiku-fives-index"),
            HaikuKey.SEVEN: search_connect("haiku-sevens-index"),
        }

    @classmethod
    def search(cls, term: str, size: HaikuKey = None) -> list[HaikuLine]:
        """Search for lines."""
        search_clients = cls.clients().values()
        if size is not None:
            search_clients = cls.clients()[size]

        results = []
        for result_set in [x.search(term, top=5) for x in search_clients]:
            for result in result_set:
                results.append(HaikuLine.from_storage_table(result))
        return results
