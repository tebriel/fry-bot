import os
from azure.data.tables import TableServiceClient

STORAGE_CONNECTION_STRING = os.getenv('STORAGE_CONNECTION_STRING')

def list_tables() -> str:
    """list all the tables we can see."""
    try:
        service = TableServiceClient.from_connection_string(
            conn_str=STORAGE_CONNECTION_STRING
        )
        results = []
        tables = service.list_tables()
        for table in tables:
            results.append(table.name)

        return ' '.join(results)
    except Exception as e:
        return f"Error: {e}"
