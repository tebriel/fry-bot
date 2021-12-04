from hikari.events.message_events import GuildMessageCreateEvent
from bot.cool_beans.storage import increment_beans

DEFAULT_BEANS = 2


async def handle(event: GuildMessageCreateEvent) -> None:
    mentions = event.message.mentions.users
    await event.message.add_reaction("\N{burrito}")
    for mention in mentions.items():
        user = mention[1]
        print(user)
        if event.author.id == user.id:
            await event.message.respond("You can't beans yourself, you're not Buddy Capps!")
        else:
            beans = increment_beans(user.id, DEFAULT_BEANS)
            await event.message.respond(f"{user.mention} was given {DEFAULT_BEANS} cool beans and now has {beans} <:coolbeans:879772252609069117>")