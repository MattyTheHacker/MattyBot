from discord.ext import commands


class Dev(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(namne='loadcog', aliases=['lc'], help='Loads a cog.')
    @commands.is_owner()
    async def loadcog(self, ctx, *, cog: str):
        """Loads a cog."""
        try:
            self.bot.load_extension(f'cogs.{cog}.cog')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unloadcog', aliases=['uc'], help='Unloads a cog.')
    @commands.is_owner()
    async def unloadcog(self, ctx, *, cog: str):
        """Unloads a cog."""
        try:
            self.bot.unload_extension(f'cogs.{cog}.cog')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


def setup(bot: commands.Bot):
    bot.add_cog(Dev(bot))
