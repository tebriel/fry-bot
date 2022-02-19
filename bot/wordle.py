import os
from azure.data.tables import TableServiceClient

STORAGE_BASE_URL = f"https://{os.getenv('STORAGE_BASE_URL')}"

def list_tables() -> str:
    """list all the tables we can see."""
    try:
        service = TableServiceClient(endpoint=STORAGE_BASE_URL)
        results = []
        tables = service.list_tables()
        for table in tables:
            results.append(table.name)

        return ' '.join(results)
    except Exception as e:
        return f"Error: {e}"
