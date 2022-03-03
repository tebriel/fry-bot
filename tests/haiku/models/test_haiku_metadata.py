from bot.haiku.models import HaikuKey


def test_from_storage_table(haiku_metadata):
    """Test the from_storage_table method."""
    metadata = haiku_metadata.from_storage_table(
        {
            "PartitionKey": "FIVE",
            "RowKey": "1",
            "MaxID": 7,
        }
    )
    assert metadata.size == HaikuKey.FIVE
    assert metadata.max_id == 7


def test_save(haiku_metadata):
    """Test the save method."""
    metadata = haiku_metadata(size=HaikuKey.FIVE, max_id=7)
    metadata.save()
    metadata.client.table_client.upsert_entity.assert_called_with(
        entity={
            "PartitionKey": HaikuKey.FIVE.value,
            "RowKey": haiku_metadata.ROW_KEY,
            "MaxID": 7,
        }
    )


def test_to_storage_dict(haiku_metadata):
    """Test the to_storage_dict method."""
    metadata = haiku_metadata(size=HaikuKey.FIVE, max_id=7)
    assert metadata.to_storage_dict() == {
        "PartitionKey": HaikuKey.FIVE.value,
        "RowKey": haiku_metadata.ROW_KEY,
        "MaxID": 7,
    }


def test_increment_id(haiku_metadata):
    """Test incrementing the ID."""
    metadata = haiku_metadata(size=HaikuKey.FIVE, max_id=7)
    metadata.increment_id()
    assert metadata.max_id == 8
    metadata.client.table_client.upsert_entity.assert_called()
