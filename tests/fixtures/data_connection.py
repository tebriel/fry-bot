from unittest.mock import Mock

import pytest
from azure.data.tables import TableClient

from bot.clients.table_client import DataConnection


@pytest.fixture
def data_connection():
    """Create a data connection with a mock client."""
    client_mock = Mock(spec_set=TableClient)
    client_mock.get_entity.return_value = None
    return DataConnection("table", client=client_mock)
