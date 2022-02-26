"""Data Storage and Retrieval objects for Haiku in Azure Data Table Storage."""
from bot.clients.table_client import DataConnection

from .formed import FormedHaiku
from .key import HaikuKey
from .line import HaikuLine
from .metadata import HaikuMetadata

conn = DataConnection("haiku")

HaikuMetadata.client = conn
HaikuLine.client = conn
FormedHaiku.client = conn
