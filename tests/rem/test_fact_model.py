from datetime import datetime

from bot.rem.model import PARTITION_KEY


def test_from_storage_table(fact):
    """Test the hydrator."""
    today = datetime.utcnow()
    entity = {
        "PartitionKey": PARTITION_KEY,
        "RowKey": "dns",
        "Author": "123123123",
        "Fact": "https://i.imgur.com/eAwdKEC.png",
        "CreatedAt": today.isoformat(),
    }
    actual = fact.from_storage_table(entity)
    assert actual.author == entity["Author"]
    assert actual.created_at == today
    assert actual.name == entity["RowKey"]
    assert actual.fact == entity["Fact"]


def test_to_storage_dict(fact):
    """Test the serializer."""
    actual = fact(
        author="123123123",
        name="dns",
        fact="https://i.imgur.com/eAwdKEC.png",
    )
    result = actual.to_storage_dict()
    assert result == {
        "PartitionKey": PARTITION_KEY,
        "RowKey": "dns",
        "Author": "123123123",
        "Fact": "https://i.imgur.com/eAwdKEC.png",
        "CreatedAt": actual.created_at.isoformat(),
    }
