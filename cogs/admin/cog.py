import logging
from discord.ext import commands


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='kill', help='Stop the bot.', hidden=False)
    @commands.is_owner()
    async def kill(self, ctx):
        logging.info('Bot is now shutting down...')
        await ctx.send('Initiating system shutdown...')
        await ctx.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
