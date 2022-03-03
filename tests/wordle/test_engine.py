from unittest.mock import Mock

import pytest

from bot.wordle.engine import Wordle


@pytest.mark.parametrize(
    "wordle_score,score_str,score,number,hard_mode,solver",
    [
        ("wordle_score", "Wordle 257 3/6*", "3", "257", True, False),
        ("wordle_score", "Wordle 257 X/6", "X", "257", False, False),
        ("wordle_score", "Wordle 257 1/6$", "1", "257", False, True),
        ("wordle_score", "Wordle 257 2/6*$", "2", "257", True, True),
    ],
    indirect=["wordle_score"],
)
def test_submit_score(wordle_score, score_str, score, number, hard_mode, solver):
    """Submit a wordle score."""
    event = Mock()
    event.content = score_str
    event.author.id = 1231812321
    Wordle.submit_score(event)
    expected_score = wordle_score(
        author=str(event.author.id),
        score=score,
        number=number,
        hard_mode=hard_mode,
        solver=solver,
    )

    wordle_score.client.table_client.upsert_entity.assert_called_with(
        entity=expected_score.to_storage_dict()
    )
