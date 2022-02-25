"""Initial Module"""
import os
import re

import hikari
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from hikari import Intents, Permissions

from bot import haiku, wordle

BOT_PERMISSIONS = (
    Permissions.VIEW_CHANNEL
    | Permissions.SEND_MESSAGES
    | Permissions.CREATE_PUBLIC_THREADS
    | Permissions.SEND_MESSAGES_IN_THREADS
    | Permissions.ADD_REACTIONS
)

bot_intents = Intents.ALL_MESSAGES | Intents.GUILD_EMOJIS | Intents.GUILD_PRESENCES

credential = DefaultAzureCredential()
secret_client = SecretClient("https://fry-bot.vault.azure.net/", credential)
secret = secret_client.get_secret("bot-gateway-token")

bot = hikari.GatewayBot(token=secret.value, intents=bot_intents)


@bot.listen()
async def listen(event: hikari.GuildMessageCreateEvent) -> None:
    """Handle incoming messages."""
    # If a non-bot user sends a message
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return
    if os.getenv("ENVIRONMENT") != "production":
        if str(event.guild_id) != "916058877722779698":
            return

    print(event.content)
    if event.content.startswith("hk.ping"):
        await event.message.respond("Pong!")
    elif event.content.startswith(".who are you"):
        await event.message.respond(f"I am {os.getenv('GITHUB_SHA')}")
    elif event.content.startswith(".rem dns"):
        await event.message.respond("http://i.imgur.com/eAwdKEC.png")
    elif event.content.startswith(".haiku"):
        await haiku.handle(event)
    elif wordle.should_handle(event):
        await wordle.handle(event)
