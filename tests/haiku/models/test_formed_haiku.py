import json
from datetime import datetime

from bot.haiku.models import HaikuKey


def test_to_storage_dict(formed_haiku):
    """Test the serializer."""
    haiku = formed_haiku(
        poem=[
            "one two three four five",
            "six seven eight nine ten",
            "six seven eight nine ten",
        ],
    )
    result = haiku.to_storage_dict()
    assert result == {
        "PartitionKey": HaikuKey.FORMED.value,
        "RowKey": haiku.created_at.isoformat(),
        "Poem": json.dumps(haiku.poem),
    }


def test_from_storage_table(formed_haiku):
    """Test the hydrator."""
    haiku = formed_haiku.from_storage_table(
        {
            "PartitionKey": HaikuKey.FORMED.value,
            "RowKey": datetime.utcnow().isoformat(),
            "Poem": json.dumps(["1", "2", "3"]),
        }
    )
    assert len(haiku.poem) == 3
