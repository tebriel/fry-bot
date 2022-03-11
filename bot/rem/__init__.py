from hikari.events.message_events import GuildMessageCreateEvent

from bot.rem.model import Fact


def should_handle(event: GuildMessageCreateEvent) -> bool:
    """Determine if the event should be handled."""
    return (event.content or "").startswith(".rem")


async def handle(event: GuildMessageCreateEvent) -> None:
    """Handle incoming events."""
    if event.content is None:
        return

    content = event.content.replace(".rem ", "")
    name = content.split(" ")[0]
    fact = " ".join(content.split(" ")[1:])

    if name == "" or name == "help":
        await event.message.respond(
            """**Remember Help**
.rem <name> - Recall a fact
.rem <name> <fact> - Remember a fact
.rem help (this help)"""
        )
    elif fact == "":
        f_data = Fact.query_by_name(name)
        if f_data is None:
            await event.message.respond(f"I don't know about {name}.")
        else:
            await event.message.respond(f_data.fact)
    else:
        entity = Fact(author=event.author, name=name, fact=fact)
        entity.save()
        await event.message.respond(f"I'll remember {name}.")
