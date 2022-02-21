#!/usr/bin/env python3
"""Convert the IDs to ints."""
from bot.clients.table_client import connect
from bot.haiku.engine import HaikuKey

if __name__ == '__main__':
    c = connect("haiku")
    for size in [HaikuKey.FIVE, HaikuKey.SEVEN]:
        entities = c.query_entities(f"PartitionKey eq '{size}'")
        for entity in entities:
            entity['RowKey'] = int(entity['RowKey'])
            c.upsert_entity(entity=entity)
            print(entity)
