from ast import alias
import discord
from discord.ext import commands
from utils import checks


class Alias(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group()
    async def alias(self, ctx: commands.Context):
        pass

    @alias.group(name='global')
    async def global_(self, ctx: commands.Context):
        pass

    @checks.mod_or_permissions(manage_guild=True)
    @alias.command(name="add")
    @commands.guild_only()
    async def _add_alias(self, ctx: commands.Context, alias_name: str, *, command):
        is_command = self.is_commnad(alias_name)
        if is_command:
            await ctx.send(f'{alias_name} is a already command, please use a different name.')
            return

        alias = await self._aliases.get_alias(ctx.guild, alias_name)
        if alias:
            await ctx.send(f'{alias_name} is already an alias.')
            return

        is_valid_name = self.is_valid_alias_name(alias_name)
        if not is_valid_name:
            await ctx.send(f'{alias_name} is not a valid alias name.')
            return

        given_command_exists = self.bot.get_command(
            command.split(maxsplit=1)[0]) is not None
        if not given_command_exists:
            await ctx.send(f'The command {command.split(maxsplit=1)[0]} does not exist.')
            return

        try:
            await self._aliases.add_alias(ctx, alias_name, command)
        except Exception as e:
            return await ctx.send(' '.join(e.args))

        await ctx.send(f'Added alias {alias_name} for {command}')

    @checks.is_owner()
    @global_.command(name='add')
    async def _add_global_alias(self, ctx: commands.Context, alias_name: str, *, command):
        is_command = self.is_command(alias_name, alias_name)
        if is_command:
            await ctx.send(f'{alias_name} is a already command, please use a different name.')
            return

        alias = await self._aliases.get_alias(None, alias_name)
        if alias:
            await ctx.send(f'{alias_name} is already an alias.')
            return

        is_valid_name = self.is_valid_alias_name(alias_name)
        if not is_valid_name:
            await ctx.send(f'{alias_name} is not a valid alias name.')
            return

        given_command_exists = self.bot.get_command(
            command.split(maxsplit=1)[0]) is not None
        if not given_command_exists:
            await ctx.send(f'The command {command.split(maxsplit=1)[0]} does not exist.')
            return

        try:
            await self._aliases.add_alias(ctx, alias_name, command, global_=True)
        except Exception as e:
            return await ctx.send(' '.join(e.args))

        await ctx.send(f'Added alias {alias_name} for {command}')

    @checks.mod_or_permissions(manage_guild=True)
    @alias.command(name='edit')
    @commands.guild_only()
    async def _edit_alias(self, ctx: commands.Context, alias_name: str, *, command):
        alias = await self._aliases.get_alias(ctx.guild, alias_name)
        if not alias:
            await ctx.send(f'Alias {alias_name} does not exist.')
            return

        given_command_exists = self.bot.get_command(
            command.split(maxsplit=1)[0]) is not None
        if not given_command_exists:
            await ctx.send(f'The command {command.split(maxsplit=1)[0]} does not exist.')
            return

        try:
            if await self._aliases.edit_alias(ctx, alias_name, command):
                await ctx.send(f'Edited alias {alias_name} for {command}')
            else:
                # Shouldn't be possible to get here...
                await ctx.send(f'Alias {alias_name} does not exist.')
        except Exception as e:
            return await ctx.send(' '.join(e.args))

    @checks.is_owner()
    @global_.command(name='edit')
    async def _edit_global_alias(self, ctx: commands.Context, alias_name: str, *, command):
        alias = await self._aliases.get_alias(None, alias_name)
        if not alias:
            await ctx.send(f'Alias {alias_name} does not exist.')
            return

        given_command_exists = self.bot.get_command(
            command.split(maxsplit=1)[0]) is not None
        if not given_command_exists:
            await ctx.send(f'The command {command.split(maxsplit=1)[0]} does not exist.')
            return

        try:
            if await self._aliases.edit_alias(ctx, alias_name, command, global_=True):
                await ctx.send(f'Edited alias {alias_name} for {command}')
            else:
                # Shouldn't be possible to get here...
                await ctx.send(f'Alias {alias_name} does not exist.')
        except Exception as e:
            return await ctx.send(' '.join(e.args))

    @alias.command(name='help')
    async def _help_alias(self, ctx: commands.Context, alias_name: str):
        alias = await self._aliases.get_alias(ctx.guild, alias_name)
        if alias:
            await self.bot.send_help_for(ctx, alias.command)
        else:
            await ctx.send(f'Alias {alias_name} does not exist.')

    @alias.command(name='show')
    async def _show_alias(self, ctx: commands.Context, alias_name: str):
        alias = await self._aliases.get_alias(ctx.guild, alias_name)
        if alias:
            await ctx.send(f'{alias_name} is an alias for the command: {alias.command}')
        else:
            await ctx.send(f'Alias {alias_name} does not exist.')

    @checks.mod_or_permissions(manage_guild=True)
    @alias.command(name='delete', aliases=['remove', 'del', 'rm'])
    @commands.guild_only()
    async def _delete_alias(self, ctx: commands.Context, alias_name: str):
        if not await self._aliases.get_guild_aliases(ctx.guild):
            await ctx.send(f'No aliases exist on server {ctx.guild}')
            return

        if await self._aliases.delete_alias(ctx, alias_name):
            await ctx.send(f'Deleted alias {alias_name}')
        else:
            await ctx.send(f'Alias {alias_name} does not exist.')

    @checks.is_owner()
    @global_.command(name='delete', aliases=['remove', 'del', 'rm'])
    async def _delete_global_alias(self, ctx: commands.Context, alias_name: str):
        if not await self._aliases.get_global_aliases():
            await ctx.send('No aliases exist.')
            return

        if await self._aliases.delete_alias(ctx, alias_name, global_=True):
            await ctx.send(f'Deleted alias {alias_name}')
        else:
            await ctx.send(f'Alias {alias_name} does not exist.')

    @alias.command(name='list')
    @commands.guild_only()
    @checks.bot_has_permissions(add_reactions=True)
    async def _list_aliases(self, ctx: commands.Context):
        aliases = await self._aliases.get_guild_aliases(ctx.guild)
        if not aliases:
            await ctx.send(f'No aliases exist on server {ctx.guild}')
            return

        paginator = commands.Paginator()
        for alias in aliases:
            paginator.add_line(f'{alias.name} - {alias.command}')

        for page in paginator.pages:
            await ctx.send(page)

    @global_.command(name='list')
    @commands.guild_only()
    @checks.bot_has_permissions(add_reactions=True)
    async def _list_alias(self, ctx: commands.Context):
        aliases = await self._aliases.get_global_aliases()
        if not aliases:
            await ctx.send('No aliases exist.')
            return

        paginator = commands.Paginator()
        for alias in aliases:
            paginator.add_line(f'{alias.name} - {alias.command}')

        for page in paginator.pages:
            await ctx.send(page)


def setup(bot: commands.Bot):
    bot.add_cog(Alias(bot))
