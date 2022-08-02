from discord.ext import commands


class Utilities(commands.Cog):

    def has_role(self, user, role_id):
        return role_id in [role.id for role in user.roles]

    def __init__(self, bot: commands.Bot):
        self.bot = bot


def setup(bot: commands.Bot):
    bot.add_cog(Utilities(bot))
