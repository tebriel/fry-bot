import pytest

from bot.haiku.models import FormedHaiku


@pytest.fixture
def formed_haiku(data_connection):
    """Create a formed haiku."""
    FormedHaiku.client = data_connection
    return FormedHaiku
