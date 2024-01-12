import discord, asyncio
from discord.ext import commands
import config
from functions.error_handling import handle_missing_argument

class Error_Handling(commands.Cog):
    """Error Handling for commands"""
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        pass
    async def cog_load(self):
        print(f'{self.__class__.__name__} has been loaded.')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if isinstance(ctx.channel, discord.DMChannel):
                return

            if isinstance(error, commands.CommandNotFound):
                return

            elif isinstance(error, discord.NotFound):
                if str(error) == '404 Not Found (error code: 10008): Unknown Message':
                    return

            elif isinstance(error, commands.MissingRequiredArgument):
                await handle_missing_argument(ctx, error)

            elif isinstance(error, commands.MissingPermissions):
                missing_permissions = ', '.join(error.missing_permissions)
                error_embed = discord.Embed(
                    title="Error",
                    description=f"You don't have the required permissions for this command, you need ``{missing_permissions}`` permission to use this command.",
                    timestamp=discord.utils.utcnow(),
                    color=config.error_color
                )
                await ctx.send(embed=error_embed, ephemeral=True)

            elif isinstance(error, commands.CommandInvokeError):
                if isinstance(error.original, asyncio.tasks.Task):
                    return
                error_embed = discord.Embed(
                    title="Error",
                    description=f"An error occurred while executing the command: {error.original}.\n\nPlease report this error to our [discord server]({config.SUPPORT_SERVER})",
                    timestamp=discord.utils.utcnow(),
                    color=config.error_color
                )
                await ctx.send(embed=error_embed, ephemeral=True)

            else:
                error_embed = discord.Embed(
                    title="Error",
                    description=f"An error occurred: {error}",
                    timestamp=discord.utils.utcnow(),
                    color=config.error_color
                )
                await ctx.send(embed=error_embed, ephemeral=True)
        except Exception as e:
            embed = discord.Embed(
                title='Error',
                description=f"Something went wrong.\n\n``{e}``",
                timestamp=discord.utils.utcnow(),
                color=config.error_color
            )
            await ctx.send(embed=embed)