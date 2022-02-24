"""Wordle Tests."""
from typing import Union

import pytest

from bot import wordle


@pytest.mark.parametrize(
    "number,expected",
    [
        ("0", True),
        (0, True),
        ("-1)", False),
        ("sdjkflds", False),
        (10000, False),
        (245, True),
        ("246", True),
    ],
)
def test_is_valid_wordle(number: Union[str, bool], expected):
    """Test is_valid_wordle."""
    assert wordle.is_valid_wordle(number) == expected
