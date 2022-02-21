#!/usr/bin/env python3

from bot.clients.table_client import connect
from bot.haiku.engine import HaikuKey

if __name__ == '__main__':
    client = connect('haiku')
    entity = client.get_entity(partition_key=str(HaikuKey.SEVEN), row_key='METADATA')
    print(entity)
