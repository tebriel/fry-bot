import re
import os
import azure
from azure.data.tables import TableServiceClient
import hikari

STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')
WORDLE_PATTERN = re.compile(r'^Wordle (?P<number>\d+) (?P<score>[\dX])/6(?P<hard_mode>\*?)(?P<solver>\$?)')
USER_PARTITION_KEY = 'user'
SCORE_PARTITION_KEY = 'score'

def connect() -> TableServiceClient:
    """connect to the table service."""
    return TableServiceClient.from_connection_string(
        conn_str=STORAGE_CONNECTION_STRING
    )

def submit_score(event: hikari.GuildMessageCreateEvent) -> None:
    """Submit a wordle score."""
    data = WORDLE_PATTERN.match(event.content)
    entity = {
        'PartitionKey': SCORE_PARTITION_KEY,
        'RowKey': f'{event.author.id}-{data.group("number")}',
        'score': data.group('score'),
        'number': data.group('number'),
        'hard_mode': data.group('hard_mode') == '*',
        'solver': data.group('solver') == '$',
    }
    print(entity)
    conn = connect()
    table_client = conn.get_table_client(table_name="wordle")
    try:
        table_client.create_entity(entity=entity)
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
