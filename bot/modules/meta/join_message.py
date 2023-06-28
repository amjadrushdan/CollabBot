import discord

from cmdClient import cmdClient

from meta import client, conf
from .lib import guide_link


message = """
Hello there i am Collab Bot.

""".format(
    guide_link=guide_link,
    support_link=conf.bot.get('support_link'),
    prefix=client.prefix
)


@client.add_after_event('guild_join', priority=0)
async def post_join_message(client: cmdClient, guild: discord.Guild):
    try:
        await guild.me.edit(nick="CollabBot")
    except discord.HTTPException:
        pass
    if (channel := guild.system_channel) and channel.permissions_for(guild.me).embed_links:
        embed = discord.Embed(
            description=message
        )
        embed.set_author(
            name="Hello everyone!",
            icon_url="https://cdn.discordapp.com/emojis/933610591459872868.webp"
        )
        try:
            await channel.send(embed=embed)
        except discord.HTTPException:
            # Something went wrong sending the hi message
            # Not much we can do about this
            pass
