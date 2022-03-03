from bot.haiku.models import HaikuKey


def test_save(haiku_metadata, haiku_line):
    """Test the save method."""
    haiku_metadata.client.table_client.get_entity.return_value = {
        "PartitionKey": HaikuKey.FIVE.value,
        "RowKey": haiku_metadata.ROW_KEY,
        "MaxID": "0",
    }
    line = haiku_line(size=HaikuKey.FIVE, line="one two three four five")
    line.save()
    line.client.table_client.upsert_entity.assert_called_with(
        entity={
            "PartitionKey": HaikuKey.FIVE.value,
            "RowKey": "1",
            "Line": "one two three four five",
            "Author": "",
        }
    )


def test_from_storage_table(haiku_line):
    """Test the hydrator."""
    line = haiku_line.from_storage_table(
        {
            "PartitionKey": HaikuKey.FIVE.value,
            "RowKey": "1",
            "Author": "1238123821",
            "Line": "one two three four five",
        }
    )
    assert line.size == HaikuKey.FIVE
    assert line.line == "one two three four five"


def test_to_storage_dict(haiku_line):
    """Test the serializer."""
    line = haiku_line(size=HaikuKey.FIVE, line="one two three four five", id_=1)
    result = line.to_storage_dict()
    assert result == {
        "PartitionKey": HaikuKey.FIVE.value,
        "RowKey": "1",
        "Author": "",
        "Line": "one two three four five",
    }
