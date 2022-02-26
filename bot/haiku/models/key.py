from enum import Enum


class HaikuKey(Enum):
    """Partition keys for the haiku table."""

    FIVE = "FIVE"
    SEVEN = "SEVEN"
    FORMED = "FORMED"
