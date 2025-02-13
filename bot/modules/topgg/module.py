from LionModule import LionModule
from LionContext import LionContext
from core.lion import Lion

from modules.sponsors.module import sponsored_commands

from .utils import get_last_voted_timestamp, lion_loveemote, lion_yayemote
from .webhook import init_webhook

module = LionModule("Topgg")

upvote_info = "You have a boost available {}, to support our project and earn **25% more LionCoins** type `{}vote` {}"


@module.launch_task
async def attach_topgg_webhook(client):
    if client.shard_id == 0:
        init_webhook()
        client.log("Attached top.gg voiting webhook.", context="TOPGG")


@module.launch_task
async def register_hook(client):
    LionContext.reply.add_wrapper(topgg_reply_wrapper)
    Lion.register_economy_bonus(economy_bonus)

    client.log("Loaded top.gg hooks.", context="TOPGG")


@module.unload_task
async def unregister_hook(client):
    Lion.unregister_economy_bonus(economy_bonus)
    LionContext.reply.remove_wrapper(topgg_reply_wrapper.__name__)

    client.log("Unloaded top.gg hooks.", context="TOPGG")

boostfree_groups = {'Meta'}
boostfree_commands = {'config', 'pomodoro','polling'}


async def topgg_reply_wrapper(func, ctx: LionContext, *args, suggest_vote=True, **kwargs):
    if not suggest_vote:
        pass
    elif not ctx.cmd:
        pass
    elif ctx.cmd.name in boostfree_commands or ctx.cmd.group in boostfree_groups:
        pass
    elif ctx.guild and ctx.guild.id in ctx.client.settings.topgg_guild_whitelist.value:
        pass
    elif ctx.guild and getattr(ctx.client.data, "premium_guilds", None) and getattr(ctx.client.data.premium_guilds, "queries", None).fetch_guild(ctx.guild.id):
        pass
    return await func(ctx, *args, **kwargs)


def economy_bonus(lion):
    return 1.25 if get_last_voted_timestamp(lion.userid) else 1
