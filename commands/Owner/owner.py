import discord, time, datetime
from discord.ext import commands
from discord import app_commands
from datetime import datetime, timedelta
import config

class Bot_Admin(commands.Cog):
    """A set of commands only to used by the bot creators."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass
    async def cog_load(self):
        print(f'{self.__class__.__name__} has been loaded.')

    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context):
        """
        Syncs all the commands to discord.

        **Usage:** sync
        """
        # Try to sync the commands
        try:
            synced_global = await ctx.bot.tree.sync()

            embed = discord.Embed(
                title="Synchronization Complete",
                description=f"Synced {len(synced_global)} commands",
                timestamp=discord.utils.utcnow(),
                color=config.main_color
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(title='❌ ERROR',
                                  description=f'**The error occured due to following reasons.\n```{e}```',
                                  color=config.error_color)
            await ctx.send(embed=embed)
            raise e