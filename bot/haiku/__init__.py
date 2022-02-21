from hikari.events.message_events import GuildMessageCreateEvent
from bot.haiku.engine import add_line, make_haiku, HaikuKey


async def handle(event: GuildMessageCreateEvent) -> None:
    """Handle incoming events."""
    if event.content.startswith('.haiku add_use_sevens'):
        haiku = add_line(HaikuKey.SEVEN, event.content.replace('.haiku add_use_sevens', ''))
    elif event.content.startswith('.haiku add_use_fives'):
        haiku = add_line(HaikuKey.FIVE, event.content.replace('.haiku add_use_sevens', ''))
    elif event.content.startswith('.haiku help'):
        await event.message.respond(""".haiku add_use_fives <five-syllable-phrase>
        .haiku add_use_sevens <seven-syllable-phrase>
        .haiku add_use_fives <seven-syllable-phrase>
        .haiku (gets you a random haiku)
        .haiku help (this help)
        """)
        return
    elif event.content.startswith('.haiku'):
        haiku = make_haiku()

    await event.message.respond(haiku)
