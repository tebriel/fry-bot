import json
import random
from enum import Enum
from datetime import datetime
from typing import List

import azure
from bot.clients.table_client import connect


class HaikuKey(Enum):
    """Partition keys for the haiku table."""
    FIVE = 'FIVE'
    SEVEN = 'SEVEN'
    FORMED = 'FORMED'


class Haiku:
    """Yet another Haiku Engine."""
    _client = None

    def _get_client(self):
        if self._client is None:
            self._client = connect("haiku")
        return self._client

    client = property(_get_client)

    def get_next_id(self, size: HaikuKey) -> int:
        """Get the next ID for a line."""
        try:
            entity = self.client.get_entity(partition_key=str(size), row_key='METADATA')
        except azure.core.exceptions.ResourceNotFoundError:
            return 0
        return int(entity.get('max_id', -1)) + 1

    def set_max_id(self, key: HaikuKey, value: int) -> None:
        """Set max id."""
        entity = {
            'PartitionKey': str(key),
            'RowKey': 'METADATA',
            'max_id': str(value)
        }
        self.client.upsert_entity(entity=entity)

    def add_line(self, size: HaikuKey, text: str) -> str:
        """Adds a line."""
        entity = {
            'PartitionKey': str(size),
            'RowKey': str(self.get_next_id(size)),
            'Line': text,
        }
        self.client.upsert_entity(entity=entity)
        self.set_max_id(size, entity['RowKey'])
        return self.make_haiku(entity)

    def random_line(self, size: HaikuKey) -> str:
        """Get a random line."""
        max_id = self.get_next_id(size) - 1
        if max_id <= 0:
            return "no data found"
        row_key = random.randint(0, max_id)
        entity = self.client.get_entity(partition_key=str(size), row_key=str(row_key))
        return entity['Line']

    def store_haiku(self, lines: List[str], c_date: str = None) -> None:
        """Store a haiku."""
        if c_date is None:
            c_date = datetime.utcnow().isoformat()
        entity = {
            'PartitionKey': str(HaikuKey.FORMED),
            'RowKey': c_date,
            'Poem': json.dumps(lines),
        }
        self.client.upsert_entity(entity=entity)

    def make_haiku(self, seed_entity=None) -> str:
        """Make a haiku."""
        lines = []
        lines.append(self.random_line(HaikuKey.FIVE))
        lines.append(self.random_line(HaikuKey.SEVEN))
        lines.append(self.random_line(HaikuKey.FIVE))
        if seed_entity is not None:
            if seed_entity['PartitionKey'] == str(HaikuKey.FIVE):
                lines[random.choice([0, 2])] = seed_entity['Line']
            else:
                lines[1] = seed_entity['Line']
        self.store_haiku(lines)
        return '\n'.join(lines)
