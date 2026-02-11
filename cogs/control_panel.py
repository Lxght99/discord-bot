import discord
from discord.ext import commands

class ControlPanel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def say(self, ctx, *, message: str):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(ControlPanel(bot))
