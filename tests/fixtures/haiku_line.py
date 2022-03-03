import pytest

from bot.haiku.models import HaikuLine


@pytest.fixture
def haiku_line(data_connection):
    """Create a haiku line."""
    HaikuLine.client = data_connection
    return HaikuLine
