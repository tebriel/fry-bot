import pytest

from bot.rem.model import Fact


@pytest.fixture
def fact(data_connection):
    """Create a formed haiku."""
    Fact.client = data_connection
    return Fact
