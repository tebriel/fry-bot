#!/usr/bin/env python3
import asyncio
import os

import hikari
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from bot import wordle

credential = DefaultAzureCredential()
secret_client = SecretClient("https://fry-bot.vault.azure.net/", credential)


async def main():
    """history of channel."""
    rest_app = hikari.RESTApp()
    secret = secret_client.get_secret("bot-gateway-token")
    async with rest_app.acquire(secret.value, "Bot") as client:
        print("a")
        msgs = await client.fetch_messages(
            channel="901164244375056384", after="929052029458984970"
        )
        print("b")
        for msg in msgs:
            if msg.content is None:
                print("empty msg")
                continue
            print(msg.content)
            if wordle.WORDLE_PATTERN.match(msg.content):
                print(msg.content)
                if wordle.submit_score(msg):
                    print(f"added msg: {msg}")


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
