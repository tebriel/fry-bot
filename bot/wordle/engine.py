"""Wordle Game Library."""
import re
from collections import defaultdict
from datetime import datetime
from typing import Union

import hikari

from bot.wordle.model import WordleScore

START = datetime(2022, 2, 19)
START_ID = 245

WORDLE_PATTERN = re.compile(
    r"^Wordle (?P<number>\d+) (?P<score>[\dX])/6(?P<hard_mode>\*?)(?P<solver>\$?)"
)
USER_PARTITION_KEY = "user"
SCORE_PARTITION_KEY = "score"


class Wordle:
    """A wordle client."""

    @staticmethod
    def is_valid_wordle(number: str) -> bool:
        """check if a wordle number is valid."""

        # Gotta be a number
        try:
            number = int(number)
        except (ValueError, TypeError):
            return False

        # Invalid
        if number < 0:
            return False

        # too far in the future
        today = datetime.utcnow()
        days = (today - START).days
        if number > START_ID + days + 1:
            return False

        return True

    @staticmethod
    def get_user_stats(author: str) -> str:
        """Gets the stats for a particular author."""
        scores: dict[str, int] = defaultdict(int)
        for result in WordleScore.query_by_author(author):
            scores[result.score] += 1

        played = sum(scores.values())
        status = f"""Statistics for <@!{author}>
Played: {played}
Win: {(played - scores['X']) / played * 100:.2f}%
"""
        return status

    @classmethod
    def get_scores(cls, number: Union[int, str] = None) -> str:
        """get the scores for a wordle."""
        if not cls.is_valid_wordle(number):
            today = datetime.utcnow()
            days = (today - START).days
            number = START_ID + days

        results: dict[str, list[str]] = defaultdict(list)

        for result in WordleScore.query_by_number(number):
            if result.author is None:
                continue
            hard_mode = r"\*" if result.hard_mode else ""
            solver = r"\$" if result.solver else ""
            score = f"<@!{result.author}>{hard_mode}{solver}"
            results[result.score].append(score)

        status = f"**Wordle {number}**\n"
        for score in sorted(results.keys()):
            status += f"{score}/6: {', '.join(results[score])}\n"
        return status

    @classmethod
    def submit_score(cls, event: hikari.GuildMessageCreateEvent) -> None:
        """Submit a wordle score."""
        data = WORDLE_PATTERN.match(event.content)
        score = WordleScore(
            author=str(event.author.id),
            score=data.group("score"),
            number=data.group("number"),
            hard_mode=data.group("hard_mode") is not None,
            solver=data.group("solver") is not None,
        )
        if not cls.is_valid_wordle(score.number):
            return False
        score.save()
        return True
