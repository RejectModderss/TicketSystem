import discord
import config


async def handle_missing_argument(ctx, error):
    param = error.param.name
    command = ctx.command
    description = command.help or "No description available."

    error_embed = discord.Embed(
        title="Information",
        timestamp=discord.utils.utcnow(),
        description=f"Missing Argument: `{param}`",
        color=config.main_color
    )
    error_embed.add_field(
        name=f"Description",
        value=f"{description}",
        inline=False
    )
    await ctx.send(embed=error_embed, ephemeral=True)
