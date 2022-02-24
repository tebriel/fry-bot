"""Wordle Game Library."""
import re
from collections import defaultdict
from datetime import datetime

import hikari

from bot.clients.table_client import connect

START = datetime(2022, 2, 19)
START_ID = 245

WORDLE_PATTERN = re.compile(
    r"^Wordle (?P<number>\d+) (?P<score>[\dX])/6(?P<hard_mode>\*?)(?P<solver>\$?)"
)
USER_PARTITION_KEY = "user"
SCORE_PARTITION_KEY = "score"


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


def get_user_stats(author: str) -> str:
    """Gets the stats for a particular author."""
    table_client = connect("wordle")
    query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and author eq '{author}'"
    scores = defaultdict(int)
    for entity in table_client.query_entities(query):
        scores[entity["score"]] += 1

    played = sum(scores.values())
    status = f"""Statistics for <@!{author}>
Played: {played}
Win: {(played - scores['X']) / played * 100:.2f}%
"""
    return status


def get_scores(number: str = None) -> str:
    """get the scores for a wordle."""
    if not is_valid_wordle(number):
        print(number)
        today = datetime.utcnow()
        days = (today - START).days
        number = START_ID + days
        print(number)
    table_client = connect("wordle")
    results = defaultdict(list)

    query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{number}'"
    for entity in table_client.query_entities(query):
        if "author" not in entity:
            continue
        score = "<@!{author}>{hard_mode}{solver}".format(
            author=entity["author"],
            hard_mode=r"\*" if entity["hard_mode"] else "",
            solver="$" if entity["solver"] else "",
        )
        results[entity["score"]].append(score)

    status = f"**Wordle {number}**\n"
    for score in sorted(results.keys()):
        status += f"{score}/6: {', '.join(results[score])}\n"
    return status


def submit_score(event: hikari.GuildMessageCreateEvent) -> None:
    """Submit a wordle score."""
    data = WORDLE_PATTERN.match(event.content)
    entity = {
        "PartitionKey": SCORE_PARTITION_KEY,
        "RowKey": f'{event.author.id}-{data.group("number")}',
        "author": str(event.author.id),
        "score": data.group("score"),
        "number": data.group("number"),
        "hard_mode": data.group("hard_mode") == "*",
        "solver": data.group("solver") == "$",
    }
    if not is_valid_wordle(entity["number"]):
        return
    table_client = connect("wordle")
    table_client.upsert_entity(entity=entity)
    return True
