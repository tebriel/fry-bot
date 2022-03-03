import pytest

from bot.wordle.model import WordleScore


@pytest.fixture
def wordle_score(data_connection):
    """Create a wordle score."""
    WordleScore.client = data_connection
    return WordleScore
