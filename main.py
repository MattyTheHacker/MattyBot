import os
import logging

from discord import DMChannel
from discord.ext import commands, tasks
from dotenv import load_dotenv

# Set creator ID
CREATOR_ID = 160478093159563266

# Set command prefix
PREFIX = '!'

# Initialise the bot
bot = commands.Bot(command_prefix=PREFIX)

ERROR_MESSAGE = f"Sorry, that doesn't look like a valid command. You can use {PREFIX}help to see my commands."
ENV_VARIABLES = ['DISCORD_TOKEN', 'BOT_ADMIN_ID']

logging.basicConfig(filename='log.txt',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


def check_env():
    failed = False
    for variable in ENV_VARIABLES:
        if not os.getenv(variable):
            logging.error(variable + 'does not exist in the .env file.')
            failed = True
    if failed:
        exit()


def get_cogs():
    cogs = []
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            cogs.append("cogs." + filename[:-3])
            logging.info(f'Found: {filename}!')
    return cogs


def load_cogs():
    for cog in get_cogs():
        bot.load_extension(cog)
        logging.info(f'Loaded: {cog}')


# Events


@bot.event
async def on_ready():
    await setup.start()


@tasks.loop(count=1)
async def setup():
    print(f'{bot.user.name} has connected to the server and is in the following channels:')
    for guild in bot.guilds:
        print(' -', guild.name)

    bot_admin = await bot.fetch_user(int(os.getenv('BOT_ADMIN_ID')))
    await bot_admin.send('Good Morning, Sir.')


@setup.before_loop
async def before_setup():
    await bot.wait_until_ready()


@bot.event
async def on_guild_join(guild):
    for channel in guild.tex_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f'wagwan my Gs what u saying? shoutout boss man <@{CREATOR_ID}>')
        break


@bot.event
async def on_message(message):
    if message.content:
        if message.content[0] == PREFIX:
            await bot.process_commands(message)
            logging.info(
                f'Command: {message.content}, recieved from user: {message.author}')
        elif isinstance(message.channel, DMChannel) and message.author != bot.user:
            await message.channel.send(ERROR_MESSAGE)
            logging.warning(
                f'Invalid Command: {message.content}, recieved from {message.author}')
    else:
        logging.error(
            'The bot seems to have recieved an empty message... Interesting...')


@bot.event
async def on_command_error(context, error):
    if isinstance(context.channel, DMChannel) and isinstance(error, commands.errors.CommandNotFound):
        await context.send(ERROR_MESSAGE)
        logging.warning(
            f'Invalid command recieved. Details Follow. Context: {context}. \n Error: {error}. \n Channel: {context.channel}')


# Startup
if __name__ == '__main__':
    load_dotenv()
    check_env()
    TOKEN = os.getenv('DISCORD_TOKEN')

    load_cogs()

    bot.run(TOKEN)
