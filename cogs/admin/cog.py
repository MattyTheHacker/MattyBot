import logging
import discord
from utils import checks
from discord.ext import commands

GENERIC_FORBIDDEN = (
    "The bot attempted to do something that is forbidden.\n The command was not executed.")

HIERARCHY_ISSUE_ADD = (
    "I can not give {role.name} to {member.mention} because that role is higher than or equal to my highest role in the Discord hierarchy.")

HIERARCHY_ISSUE_REMOVE = (
    "I can not remove {role.name} from {member.mention} because that role is higher than or equal to my highest role in the Discord hierarchy.")

ROLE_HIERARCHY_ISSUE = (
    "I can not edit {role.name} because that role is higher than my or equal to highest role in the Discord hierarchy.")

USER_HIERARCHY_ISSUE_ADD = (
    "I can not let you give {role.name} to {member.mention} because that role is higher than or equal to your highest role in the Discord hierarchy.")

USER_HIERARCHY_ISSUE_REMOVE = (
    "I can not let you remove {role.name} from {member.mention} because that role is higher than or equal to your highest role in the Discord hierarchy.")

ROLE_USER_HIERARCHY_ISSUE = (
    "I can not let you edit {role.name} because that role is higher than or equal to your highest role in the Discord hierarchy.")

NEED_MANAGE_ROLES = ('I need the "Manage Roles" permission to do that.')


class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def role_hierarchy_check(ctx: commands.Context, role: discord.Role) -> bool:
        """
        Checks if the bot has the role or higher than the role.
        :param ctx:
        :param role: Role object.
        :return: True if the user has the role or higher than the role.
        """
        return ctx.guild.me.top_role > role

    @staticmethod
    def user_hierarchy_check(ctx: commands.Context, role: discord.Role) -> bool:
        """
        Checks if the user has permission to edit the given role
        :param ctx:
        :param role: Role object.
        :return: True if the user has permission to edit the given role.
        """
        return ctx.author.top_role > role or ctx.author == ctx.guild.owner

    async def _addrole(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, check_user=True):
        """
        Adds a role to a member.
        :param ctx:
        :param member: Member object to which the role is to be added.
        :param role: Role object to be added to the member.
        """
        if role in member.roles:
            await ctx.send(f"{member.mention} already has the role {role.name}.")
            return
        if check_user and not self.user_hierarchy_check(ctx, role):
            await ctx.send((USER_HIERARCHY_ISSUE_ADD).format(role=role, member=member))
            return
        if not self.role_hierarchy_check(ctx, role):
            await ctx.send((HIERARCHY_ISSUE_ADD).format(role=role, member=member))
            return
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send(NEED_MANAGE_ROLES)
            return
        try:
            await member.add_roles(role)
        except discord.Forbidden:
            await ctx.send(GENERIC_FORBIDDEN)
        else:
            await ctx.send(f"{member.mention} has been given the role {role.name}.")

    async def _removerole(self, ctx: commands.Context, member: discord.Member, role: discord.Role, *, check_user=True):
        """
        Removes a role from a member.
        :param ctx:
        :param member: Member object from which the role is to be removed.
        :param role: Role object to be removed from the member.
        """
        if role not in member.roles:
            await ctx.send(f"{member.mention} does not have the role {role.name}.")
            return
        if check_user and not self.user_hierarchy_check(ctx, role):
            await ctx.send((USER_HIERARCHY_ISSUE_REMOVE).format(role=role, member=member))
            return
        if not self.role_hierarchy_check(ctx, role):
            await ctx.send((HIERARCHY_ISSUE_REMOVE).format(role=role, member=member))
            return
        if not ctx.guild.me.guild_permissions.manage_roles:
            await ctx.send(NEED_MANAGE_ROLES)
            return
        try:
            await member.remove_roles(role)
        except discord.Forbidden:
            await ctx.send(GENERIC_FORBIDDEN)
        else:
            await ctx.send(f'{member.mention} has been removed from the role {role.name}.')

    @commands.command(name='addrole', aliases=['ar'], help='Adds a role to a member.')
    @commands.guild_only()
    @checks.admin_or_permissions(manage_roles=True)
    async def addrole(self, ctx: commands.Context, rolename: discord.Role, *, user: discord.Member = None):
        """
        Adds a role to a member.
        If no user is given, the role is added to the author.
        If the role contains a space use double quotes.
        :param ctx:
        :param rolename: Name of the role to be added.
        :param user: User object to which the role is to be added.
        """
        if user is None:
            user = ctx.author
        await self._addrole(ctx, user, rolename)

    @commands.command(name='removerole', aliases=['rr'], help='Removes a role from a member.')
    @commands.guild_only()
    @checks.admin_or_permissions(manage_roles=True)
    async def removerole(self, ctx: commands.Context, rolename: discord.Role, *, user: discord.Member = None):
        """
        Removes a role from a member.
        If no user is given, the role is removed from the author.
        If the role contains a space use double quotes.
        :param ctx:
        :param rolename: Name of the role to be removed.
        :param user: User object from which the role is to be removed.
        """
        if user is None:
            user = ctx.author
        await self._removerole(ctx, user, rolename)

    @commands.command(name='kill', help='Stop the bot.', hidden=False)
    @commands.is_owner()
    async def kill(self, ctx):
        logging.info('Bot is now shutting down...')
        await ctx.send('Initiating system shutdown...')
        await ctx.bot.close()


def setup(bot: commands.Bot):
    bot.add_cog(Admin(bot))
