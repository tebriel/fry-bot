import pytest

from bot.haiku.models import HaikuMetadata


@pytest.fixture()
def haiku_metadata(data_connection):
    """Create a haiku metadata."""
    HaikuMetadata.client = data_connection
    return HaikuMetadata
