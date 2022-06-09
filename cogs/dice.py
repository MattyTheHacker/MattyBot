from discord.ext import commands
from random import randint
import logging


class Dice(commands.Cog, name='Random'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: str):
        try:
            rolls = []
            qty, sides = dice.split('d')
            await ctx.send(f'Rolling a {sides} sided die {qty} times...')
            for i in range(int(qty)):
                roll = randint(1, int(sides))
                rolls.append(f'{roll} ')
            await ctx.send(rolls)
        except ValueError:
            await ctx.send('Invalid dice format. Please use [qty]d[sides]. (e.g. 2d6 will produce 2 dice with 6 sides each')
            logging.warning(f'Invalid dice format, provided: {dice}')


def setup(bot: commands.Bot):
    bot.add_cog(Dice(bot))
