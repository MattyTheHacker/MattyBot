from discord.ext import commands


class Pong(commands.Cog, name='Pong Cog'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send('Pong')

    @commands.command()
    async def pong(self, ctx: commands.Context):
        await ctx.send('Ping')


def setup(bot: commands.Bot):
    bot.add_cog(Pong(bot))
