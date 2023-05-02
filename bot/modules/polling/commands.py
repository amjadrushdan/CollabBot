import re
import discord
from .module import module

@module.cmd(
    name="poll",
    desc="Create a new poll",
    group="Productivity",
    aliases=('polling','polls'),
)
async def cmd_poll(ctx):
    """
    Usage``:
        !poll <This is a question>, <Option 1>, <Option 2>, [Option 3]
    Description:
        Creates a new poll with the specified question and options
    Example``:
        !poll What's your favorite color?, Red, Green, Blue
    """
    # Split the arguments into the question and options
    split_args = ctx.arg_str.split(",")
    
    if len(split_args) < 3:
        await ctx.error_reply("Please provide at least 2 options.\n"
                              "Example: `!poll This is a question, Option 1, Option 2`")
        return
    elif len(split_args) > 11:
        await ctx.error_reply("Sorry, I can only accept up to 10 options.\n"
                              "Example: `!poll This is a question, Option 1, Option 2, Option 3`")
        return
    
    # Get the question and options
    question = split_args[0].strip()
    options = [o.strip() for o in split_args[1:]]
    
    # Define the emoji reactions
    emoji_list = ["\U0001F1E6", "\U0001F1E7", "\U0001F1E8", "\U0001F1E9",
                  "\U0001F1EA", "\U0001F1EB", "\U0001F1EC", "\U0001F1ED",
                  "\U0001F1EE", "\U0001F1EF"]
    
    # Create the poll embed
    poll_embed = discord.Embed(
        title=f"Poll: {question}",
        color=discord.Colour.orange(),
        description="")
    for i in range(len(options)):
        if i >= 10:
            break
        poll_embed.add_field(name=f"{emoji_list[i]} {options[i]}", value="\u200b", inline=False)
    
    # Send the poll message
    poll_msg = await ctx.reply(embed=poll_embed)
    
    # Add emoji reactions to each option
    for i in range(len(options)):
        if i >= 10:
            break
        await poll_msg.add_reaction(emoji_list[i])