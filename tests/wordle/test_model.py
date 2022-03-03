from bot.wordle.model import SCORE_PARTITION_KEY


def test_from_storage_table(wordle_score):
    """Test the hydrator."""
    score = wordle_score.from_storage_table(
        {
            "PartitionKey": SCORE_PARTITION_KEY,
            "RowKey": "test-1",
            "author": "test",
            "score": 1,
            "number": 1,
            "hard_mode": False,
            "solver": True,
        }
    )
    assert score.author == "test"
    assert score.score == 1
    assert score.number == 1
    assert score.hard_mode is False
    assert score.solver is True


def test_to_storage_dict(wordle_score):
    """Test the serializer."""
    score = wordle_score(author="test", score=1, number=1, hard_mode=False, solver=True)
    result = score.to_storage_dict()
    assert result == {
        "PartitionKey": SCORE_PARTITION_KEY,
        "RowKey": "test-1",
        "author": "test",
        "score": 1,
        "number": 1,
        "hard_mode": False,
        "solver": True,
    }
