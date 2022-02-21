from enum import Enum

from bot.clients.table_client import connect


class HaikuKey(Enum):
    """Partition keys for the haiku table."""
    FIVE = 1
    SEVEN = 2
    FORMED = 3


def get_next_id(size: HaikuKey) -> int:
    """Get the next ID for a line."""
    client = connect("haiku")
    entity = client.get_entity(partition_key=str(size), row_key='METADATA')
    if entity is None:
        return 1
    return int(entity['max_id']) + 1


def set_max_id(key: HaikuKey, value: int) -> None:
    """Set max id."""
    entity = {
        'PartitionKey': str(key),
        'RowKey': 'METADATA',
        'max_id': str(value)
    }
    client = connect("haiku")
    client.upsert_entity(entity=entity)


def add_line(size: HaikuKey, text: str) -> str:
    """Adds a line."""
    entity = {
        'PartitionKey': str(size),
        'RowKey': str(get_next_id(size)),
        'Line': text,
    }
    client = connect("haiku")
    client.upsert_entity(entity=entity)
    return str(entity)


def make_haiku() -> str:
    """Make a haiku."""
    return "a haiku"
