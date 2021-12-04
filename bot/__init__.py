"""Initial Module"""
import os
import hikari
from hikari import Permissions, Intents
from bot import cool_beans

bot_permissions = (
    Permissions.VIEW_CHANNEL
    | Permissions.SEND_MESSAGES
    | Permissions.CREATE_PUBLIC_THREADS
    | Permissions.SEND_MESSAGES_IN_THREADS
    | Permissions.ADD_REACTIONS
)

bot_intents = (
    Intents.ALL_MESSAGES
    | Intents.GUILD_EMOJIS
    | Intents.GUILD_PRESENCES
)

bot = hikari.GatewayBot(token=os.getenv('BOT_GATEWAY_TOKEN'), intents=bot_intents)

@bot.listen()
async def ping(event: hikari.GuildMessageCreateEvent) -> None:
    """Handle ping event."""
    # If a non-bot user sends a message "hk.ping", respond with "Pong!"
    # We check there is actually content first, if no message content exists,
    # we would get `None' here.
    if event.is_bot or not event.content:
        return

    if event.content.startswith("hk.ping"):
        await event.message.respond("Pong!")
    elif event.content.startswith(".who are you"):
        await event.message.respond(f"I am {os.getenv('GITHUB_SHA')}")
    elif "taco johns" in event.content:
        await event.message.add_reaction("🌮")
        await event.message.respond("Nachos navidad?!")
    elif event.content.startswith(".cool beans"):
        await cool_beans.handle(event)

if __name__ == '__main__':
    bot.run()