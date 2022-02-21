#!/usr/bin/env python3
"""Load the haiku data."""
import gzip
import json
from bot.haiku.engine import Haiku, HaikuKey

if __name__ == '__main__':
    with gzip.open('./seeds/haiku_db.json') as db:
        haiku = json.load(db)

    h = Haiku()
    for line in haiku:
        size = None
        if line.get('syllables') == 5:
            size = HaikuKey.FIVE
        elif line.get('syllables') == 7:
            size = HaikuKey.SEVEN
        else:
            print(f"Unknown size: {line}")
            continue
        h.add_line(size, line['message'])
