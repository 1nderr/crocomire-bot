from asyncio import TimeoutError
from discord import Message
from discord.ext.commands import Context

timeout = 20.0
red_circle: str = "🔴"


# Waits for the user to press the red button reaction to proceed
async def confirm(ctx: Context, resp: Message) -> bool:
    await resp.add_reaction(red_circle)
    try:
        # This loop prevents a bug where if you did two stats cmds and reacted to one of them,
        # it would send the follow up message to both messages instead of the one that was reacted to.
        while True:
            await ctx.bot.wait_for('reaction_add',
                                   timeout=timeout,
                                   check=lambda react, user: str(react.emoji) == red_circle and user == ctx.author)

            resp = await ctx.channel.fetch_message(resp.id)
            if resp.reactions[0].count > 1:
                return True

    except TimeoutError:
        return False
