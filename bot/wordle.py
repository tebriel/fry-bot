"""Wordle Game Library."""
import re
from collections import defaultdict
from datetime import datetime

import azure
import hikari
from azure.identity import DefaultAzureCredential
from azure.data.tables import TableServiceClient

START = datetime(2022, 2, 19)
START_ID = 245

WORDLE_PATTERN = re.compile(r'^Wordle (?P<number>\d+) (?P<score>[\dX])/6(?P<hard_mode>\*?)(?P<solver>\$?)')
USER_PARTITION_KEY = 'user'
SCORE_PARTITION_KEY = 'score'


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


def connect() -> TableServiceClient:
    """connect to the table service."""
    credential = DefaultAzureCredential()
    client = TableServiceClient(
        endpoint="https://frybot.table.core.windows.net/",
        credential=credential
    )
    return client


def get_user_stats(author: str) -> str:
    """Gets the stats for a particular author."""
    conn = connect()
    table_client = conn.get_table_client(table_name="wordle")
    query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and author eq '{author}'"
    scores = defaultdict(int)
    try:
        for entity in table_client.query_entities(query):
            scores[entity['score']] += 1

        played = sum(scores.values())
        status = f'''Statistics for <@!{author}>
Played: {played}
Win: {(played - scores['X']) / played * 100:.2f}%
'''
        return status
    except Exception as e:
        print(entity)
        return f"Error: {e}"


def get_scores(number: str = None) -> str:
    """get the scores for a wordle."""
    if not is_valid_wordle(number):
        print(number)
        today = datetime.utcnow()
        days = (today - START).days
        number = START_ID + days
        print(number)
    conn = connect()
    table_client = conn.get_table_client(table_name="wordle")
    results = defaultdict(list)

    query = f"PartitionKey eq '{SCORE_PARTITION_KEY}' and number eq '{number}'"
    try:
        for entity in table_client.query_entities(query):
            if 'author' not in entity:
                continue
            score = "<@!{author}>{hard_mode}{solver}".format(
                author=entity['author'],
                hard_mode=r'\*' if entity['hard_mode'] else '',
                solver='$' if entity['solver'] else ''
            )
            results[entity['score']].append(score)

        status = f'**Wordle {number}**\n'
        for score in sorted(results.keys()):
            status += f"{score}/6: {', '.join(results[score])}\n"
        return status
    except Exception as e:
        print(entity)
        return f"Error: {e}"


def submit_score(event: hikari.GuildMessageCreateEvent) -> None:
    """Submit a wordle score."""
    data = WORDLE_PATTERN.match(event.content)
    entity = {
        'PartitionKey': SCORE_PARTITION_KEY,
        'RowKey': f'{event.author.id}-{data.group("number")}',
        'author': str(event.author.id),
        'score': data.group('score'),
        'number': data.group('number'),
        'hard_mode': data.group('hard_mode') == '*',
        'solver': data.group('solver') == '$',
    }
    if not is_valid_wordle(entity['number']):
        return
    conn = connect()
    table_client = conn.get_table_client(table_name="wordle")
    try:
        table_client.upsert_entity(entity=entity)
        return True
    except azure.core.exceptions.ResourceExistsError:
        print('Entity already exists', entity)
        return False


def list_tables() -> str:
    """list all the tables we can see."""
    try:
        results = []
        tables = connect().list_tables()
        for table in tables:
            results.append(table.name)

        return ' '.join(results)
    except Exception as e:
        return f"Error: {e}"
