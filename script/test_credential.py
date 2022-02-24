#!/usr/bin/env python3
"""Test script for Azure credentials."""

import azure

from bot.clients.table_client import connect
from bot.haiku.engine import HaikuKey

if __name__ == "__main__":
    client = connect("haiku")
    try:
        entity = client.get_entity(
            partition_key=str(HaikuKey.SEVEN), row_key="METADATA"
        )
        print(entity)
    except azure.core.exceptions.ResourceNotFoundError:
        client.upsert_entity(
            entity={
                "PartitionKey": str(HaikuKey.SEVEN),
                "RowKey": "METADATA",
            }
        )
        print("Upserted item")
