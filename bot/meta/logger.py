import sys
import logging
import asyncio
from discord import AllowedMentions

from cmdClient.logger import cmd_log_handler

from utils.lib import mail, split_text

from .client import client
from .config import conf


# Setup the logger
logger = logging.getLogger()
log_fmt = logging.Formatter(fmt='[{asctime}][{levelname:^8}] {message}', datefmt='%d/%m | %H:%M:%S', style='{')
term_handler = logging.StreamHandler(sys.stdout)
term_handler.setFormatter(log_fmt)
logger.addHandler(term_handler)
logger.setLevel(logging.INFO)


# Define the context log format and attach it to the command logger as well
@cmd_log_handler
def log(message, context="GLOBAL", level=logging.INFO, post=True):
    # Add prefixes to lines for better parsing capability
    lines = message.splitlines()
    if len(lines) > 1:
        lines = [
            '┌ ' * (i == 0) + '│ ' * (0 < i < len(lines) - 1) + '└ ' * (i == len(lines) - 1) + line
            for i, line in enumerate(lines)
        ]
    else:
        lines = ['─ ' + message]

    for line in lines:
        logger.log(level, '\b[{}] {}'.format(
            str(context).center(22, '='),
            line
        ))

    # Fire and forget to the channel logger, if it is set up
    if post and client.is_ready():
        asyncio.ensure_future(live_log(message, context, level))


# Live logger that posts to the logging channels
async def live_log(message, context, level):
    if level >= logging.INFO:
        log_chid = conf.bot.getint('log_channel')

        # Generate the log messages
        header = "[{}][{}]".format(logging.getLevelName(level), str(context))
        if len(message) > 1900:
            blocks = split_text(message, blocksize=1900, code=False)
        else:
            blocks = [message]

        if len(blocks) > 1:
            blocks = [
                "```md\n{}[{}/{}]\n{}\n```".format(header, i+1, len(blocks), block) for i, block in enumerate(blocks)
            ]
        else:
            blocks = ["```md\n{}\n{}\n```".format(header, blocks[0])]

        # Post the log messages
        if log_chid:
            [await mail(client, log_chid, content=block, allowed_mentions=AllowedMentions.none()) for block in blocks]


# Attach logger to client, for convenience
client.log = log
