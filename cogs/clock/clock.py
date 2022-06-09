from datetime import datetime

import discord
from discord.ext import commands
from utils.dates import format_date, get_clock_emoji
from utils.embedder import build_embed
from art import text2art

def get_embed_title(message: discord.Message) -> str:
    return message.embeds[0].title

def clock_embed() -> discord.Embed:
    now = datetime.utcnow()
    clock = get_clock_emoji(now)
    return build_embed(title=f'{clock} It is now {format_date(now)} UTC', description=f'stuff')

async def get_or_create_message(bot: commands.Bot, channel:discord.TextChannel) -> discord.Message:
    message = await channel.history(limit=20).get(author__id=bot.user.id)

    if not message:
        message = await channel.send(embed=clock_embed())
    return message

def new_channel_name() -> str:
    now = datetime.utcnow()
    rounded = now.replace(minute=now.minute // 10 * 10)
    return f"clock︱~{rounded.strftime('%H:%M')}・𝖴𝖳𝖢"









