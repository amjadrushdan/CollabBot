
import re
import discord
from .module import module

@module.cmd(
    name="polling",
    desc="Create new poll",
    group="Productivity",
    aliases=('poll','polls'),
)
async def cmd_polling(ctx):
    """
    Usage``:
        {prefix}poll "question" "option A" "option B"
    Description:
        Creates a new poll with the specified question and options
    Example``:
        {prefix}poll "Class time" "2:00PM" "3:00PM"
    """
    split_args = re.findall(r'"([^"]+)"', ctx.args)
    
    if len(split_args) < 2:
        await ctx.error_reply("Please provide at least 2 options.\n"
                            """`!poll "question" "option A" "option B"`"""
                              )
        return
    elif len(split_args) == 2:
        await ctx.error_reply("Please provide at least one more option.\n"
                            """`!poll "question" "option A" "option B"`"""
                              )
        return
    elif len(split_args) > 10:
        await ctx.error_reply("Sorry, I can only accept up to 10 options.\n"
                            """`!poll "question" "option A" "option B"`"""
                              )
        return
    
    question = split_args[0].strip()
    options = split_args[1:]      

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

    
    
    
    
    
    
        
    
    
    

