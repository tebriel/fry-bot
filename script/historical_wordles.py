#!/usr/bin/env python3
import os
import asyncio
import hikari
from bot import wordle


async def main():
    """history of channel."""
    rest_app = hikari.RESTApp()
    async with rest_app.acquire(os.getenv('BOT_GATEWAY_TOKEN'), "Bot") as client:
        print('a')
        msgs = await client.fetch_messages(channel='901164244375056384', after='929052029458984970')
        print('b')
        for msg in msgs:
            if msg.content is None:
                print('empty msg')
                continue
            print(msg.content)
            if wordle.WORDLE_PATTERN.match(msg.content):
                print(msg.content)
                if wordle.submit_score(msg):
                    print(f'added msg: {msg}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
