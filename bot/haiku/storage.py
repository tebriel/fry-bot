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
    entity = client.get_entity(partition_key=size, row_key='METADATA')
    if entity is None:
        return 1
    return int(entity['max_id']) + 1


def add_line(size: HaikuKey, text: str) -> str:
    """Adds a line."""
    entity = {
        'PartitionKey': size,
        'RowKey': text
    }
    client = connect("haiku")
    client.upsert_entity(entity=entity)


def increment_beans(user_id: str, count: int) -> int:
    """Increment beans."""
    client = connect().get_blob_client(container, str(user_id))
    if client.exists():
        beans = int(client.download_blob().readall().decode())
        client.delete_blob()
    else:
        beans = 0
    beans += count
    client.upload_blob(str(beans).encode())
    return beans
