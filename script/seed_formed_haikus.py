#!/usr/bin/env python3
"""Load the haiku data."""
import gzip
import json
from datetime import datetime
from bot.haiku.engine import Haiku

if __name__ == '__main__':
    with gzip.open('./seeds/haiku_db.json.gz') as db:
        haiku = json.load(db)

    h = Haiku()
    for line in haiku:
        if 'poem' not in line:
            continue
        c_date = datetime.strptime(line['date'], '%b %d %Y %H:%M:%S')
        print(line['date'], c_date.isoformat())
        
        h.store_haiku(line['poem'], c_date=c_date.isoformat())
