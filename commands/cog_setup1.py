from discord.ext import commands
from commands.Everything.everything import Everything
from commands.Owner.owner import Bot_Admin
from commands.Error_Handling.Error_Handling import Error_Handling


async def setup(bot:commands.Bot):
    await bot.add_cog(Everything(bot))
    await bot.add_cog(Bot_Admin(bot))
    await bot.add_cog(Error_Handling(bot))












