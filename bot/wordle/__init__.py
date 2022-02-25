"""Handle Wordle Commands."""
from hikari.events.message_events import GuildMessageCreateEvent

from bot.wordle.engine import WORDLE_PATTERN, Wordle

wordle = Wordle()


def should_handle(event: GuildMessageCreateEvent) -> bool:
    """Should this event be handled?"""
    return bool(event.content.startswith(".wordle") or WORDLE_PATTERN.match(
        event.content
    ))


async def handle(event: GuildMessageCreateEvent) -> None:
    """Handle incoming events."""
    content = event.content.replace(".wordle", "").strip()
    command = content.split(" ")[0]

    if WORDLE_PATTERN.match(event.content):
        if wordle.submit_score(event):
            await event.message.add_reaction("👀")
    elif command in ["me"]:
        await event.message.respond(wordle.get_user_stats(event.author.id))
    elif wordle.is_valid_wordle(command) or command == "":
        await event.message.respond(wordle.get_scores(command), user_mentions=False)
    else:
        await event.message.respond(
            """**Wordle Help**
.wordle <number> # Gets the wordle for that number
.wordle # Gets the wordle for today
.wordle help (this help)"""
        )
