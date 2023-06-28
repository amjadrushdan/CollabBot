
import datetime
import re
import discord
from .module import module
from .data import email_data

@module.cmd(
    name="email",
    desc="Register email for remainders notification",
    group="Productivity",
    aliases=('emails','mail'),
)
async def cmd_poll(ctx):
    """
    Usage``:
        !email <youremail@gmail.com>
    Description:
        Register your email to receive notification
    Example``:
        !email collabbot@gmail.com
    """
    
    # Extract the email from the message content
    email = ctx.arg_str.split(" ")

    # Check if the user provided an email address
    if len(email) < 0 or not re.match(r"[^@]+@[^@]+\.[^@]+", email[0]):
        error_embed = discord.Embed(
            description="Please provide a valid email address.\n```!email <youremail@gmail.com>\n\nExample : !email collabbot@gmail.com```",
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        )
        await ctx.reply(embed=error_embed)
        return
    
    update_email(email,ctx)
    
    embed = discord.Embed(
        description=f"Email '{email[0]}' registered successfully.",
        colour=discord.Colour.orange(),
        timestamp=datetime.datetime.utcnow()
    ).set_author(
        name="Email for {}".format(ctx.author.display_name),
        icon_url=ctx.author.avatar_url
        )

    await ctx.reply(embed=embed)

# Update the user's email in the database
def update_email(email,ctx):
    email_data.update_where(
        {'useremail': email[0]},
        userid= ctx.author.id
    )

    
