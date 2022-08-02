import logging
import discord
from discord.errors import HTTPException
from discord.ext import commands
from discord.ext.tasks import loop

from .clock import (clock_embed, get_or_create_message,
                    new_channel_name, get_embed_title)

CLOCK_CHANNEL_ID = 1


class Clock(commands.Cog, name="Clock"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.clock.start()
        logging.info('Starting Clock...')

    @loop(seconds=1)
    async def clock(self):
        try:
            embed = clock_embed()
            if embed.title != get_embed_title(self.__message):
                await self.__message.edit(embed=embed)
        except HTTPException:
            self.__message = await get_or_create_message(self.__bot, self.__channel)

        channel_name = new_channel_name()
        if self.__channel.name != channel_name:
            await self.__channel.edit(name=channel_name)

    @clock.before_loop
    async def clock_init(self) -> None:
        self.__channel = self.__bot.get_channel(CLOCK_CHANNEL_ID)
        if not isinstance(self.__channel, discord.TextChannel):
            logging.warning('Channel not found...')
            return self.clock.cancel()
        self.__message = await get_or_create_message(self.__bot, self.__channel)


def setup(bot):
    bot.add_cog(Clock(bot))
