from hikari.events.message_events import GuildMessageCreateEvent
from bot.haiku.engine import Haiku, HaikuKey

haiku = Haiku()

async def handle(event: GuildMessageCreateEvent) -> None:
    """Handle incoming events."""
    content = event.content.replace('.haiku ', '')
    command = content.split(' ')[0]
    data = ' '.join(content.split(' ')[1:])

    if command in ['add_sevens', 'add_use_sevens']:
        result = haiku.add_line(HaikuKey.SEVEN, data)
    elif command in ['add_fives', 'add_use_fives']:
        result = haiku.add_line(HaikuKey.FIVE, data)
    elif command in ['from', 'about']:
        result = haiku.about(data)
    elif event.content == '.haiku':
        result = haiku.make_haiku()
    else:
        await event.message.respond("""**Haiku Help**
.haiku add_fives <seven-syllable-phrase>
.haiku add_sevens <seven-syllable-phrase>
.haiku about <search term>
.haiku (gets you a random haiku)
.haiku help (this help)""")
        return

    await event.message.respond(result)
