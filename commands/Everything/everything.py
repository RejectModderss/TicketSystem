import discord, os
from discord.ext import commands
from discord import app_commands
from datetime import datetime

import config
from views.buttons import ticket_launcher, confirm


class Everything(commands.Cog):
    """A set of commands that can be fun for everyone."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        pass

    async def cog_load(self):
        print(f'{self.__class__.__name__} has been loaded.')

    @commands.hybrid_command(name='ticket', description='Launches the ticketing system')
    @app_commands.default_permissions(manage_guild=True)
    @app_commands.checks.cooldown(3, 60, key=lambda i: (i.guild_id))
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @app_commands.checks.has_role(roleid)
    @commands.guild_only()
    async def ticketing(self, ctx):
        support_description = (
            "- 👷 • **Support:** Developers, Admins, and Mods will all see this ticket. This ticket is for support, so we can all help you. When you open this ticket, please explain what you need help with or what you require from staff so that we can assist you effectively when we see the ticket."
        )

        apply_for_staff_description = (
            "- ✅ • **Apply For Staff:** Developers and Admins will all see this ticket. This ticket is for applying for staff positions. When you open this ticket, please provide any relevant information and express your interest in joining the staff team."
        )

        report_user_description = (
            "- 🚨 • **Report User:** Use this category to report any rule violations, harassment, or suspicious activities by other users. Admins will review and take appropriate actions."
        )

        disclaimer_warning = (
            "- **__Disclaimer:__** Please ensure you use the correct ticket for your intended purpose. Opening the wrong ticket will result in your ticket being closed without exception."
        )

        warning_message = (
            "- **__⚠️WARNING⚠️: __**If you open ANY ticket for purposes other than what's specified above (e.g., **__bug reporting__** or **__suggestions__**), your ticket will be closed or ignored."
        )

        description = f"{support_description}\n\n{apply_for_staff_description}\n\n{report_user_description}\n\n{disclaimer_warning}\n\n{warning_message}"

        embed = discord.Embed(title="Request Support, Apply For Staff, or Report a User", description=description, color=config.main_color)
        await ctx.channel.send(embed=embed, view=ticket_launcher(self.bot))
        await ctx.send("Ticket system is now launched!", ephemeral=True)

    @commands.hybrid_command(name='close', description='Closes the ticket')
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def close(self, ctx):
        allowed_channel_names = ["support-ticket", "report-user-ticket", "staff-application-ticket"]
        required_role_id = roleid

        member = ctx.author
        required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)

        if required_role in member.roles:
            if any(name in ctx.channel.name for name in allowed_channel_names):
                ticket_channel = ctx.guild.get_channel(ctx.channel.id)
                transcript_channel_id = channelid
                confirm_view = confirm(ticket_channel, transcript_channel_id, self.bot)
                embed = discord.Embed(title="Are you sure you want to close this ticket?",
                                      color=discord.Colour.blurple())
                await ctx.send(embed=embed, view=confirm_view, ephemeral=True)
            else:
                await ctx.send("This isn't a ticket!", ephemeral=True)
        else:
            await ctx.send("Only Staff can close the ticket!", ephemeral=True)

    @commands.hybrid_command(name='add', description='Adds a user to the ticket')
    @app_commands.describe(user="The user you want to add to the ticket")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(3, 20, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def add(self, ctx, user: discord.Member):
        allowed_channel_names = ["support-ticket", "report-user-ticket", "staff-application-ticket"]
        required_role_id = roleid

        member = ctx.author
        required_role = discord.utils.get(ctx.guild.roles, id=required_role_id)

        if required_role in member.roles:
            if any(name in ctx.channel.name for name in allowed_channel_names):
                await ctx.channel.set_permissions(user, view_channel=True, send_messages=True, attach_files=True,
                                                  embed_links=True)
                await ctx.send(f"{user.mention} has been added to the ticket by {ctx.author.mention}!")
            else:
                await ctx.send("This isn't a supported ticket channel!", ephemeral=True)
        else:
            await ctx.send("Only Staff can add users to the ticket!", ephemeral=True)

    @commands.hybrid_command(name='remove', description='Removes a user from the ticket')
    @app_commands.describe(user="The user you want to remove from the ticket")
    @app_commands.default_permissions(manage_channels=True)
    @app_commands.checks.cooldown(3, 20, key=lambda i: (i.guild_id, i.user.id))
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    @commands.guild_only()
    async def remove(self, ctx, user: discord.Member):
        allowed_channel_names = ["support-ticket", "report-user-ticket", "staff-application-ticket"]

        if any(name in ctx.channel.name for name in allowed_channel_names):
            if type(self.bot.ticket_mod) is not discord.Role:
                self.bot.ticket_mod = ctx.guild.get_role(roleid)

            if self.bot.ticket_mod not in ctx.author.roles:
                return await ctx.send("You aren't authorized to do this!", ephemeral=True)

            if self.bot.ticket_mod not in user.roles:
                await ctx.channel.set_permissions(user, overwrite=None)
                await ctx.send(f"{user.mention} has been removed from the ticket by {ctx.author.mention}!")
            else:
                await ctx.send(f"{user.mention} is a moderator!", ephemeral=True)
        else:
            await ctx.send("This isn't a supported ticket channel!", ephemeral=True)

    @commands.hybrid_command(name='transcript', description='Generates a transcript for a ticket')
    @commands.guild_only()
    async def transcript(self, ctx):
        allowed_channel_names = ["support-ticket", "report-user-ticket", "staff-application-ticket"]

        if any(name in ctx.channel.name for name in allowed_channel_names):
            await ctx.defer()
            if os.path.exists(f"{ctx.channel.id}.md"):
                return await ctx.send(f"A transcript is already being generated!", ephemeral=True)
            with open(f"{ctx.channel.id}.md", 'a') as f:
                f.write(f"# Transcript of {ctx.channel.name}:\n\n")
                async for message in ctx.channel.history(limit=None, oldest_first=True):
                    created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                    if message.edited_at:
                        edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                        f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                    else:
                        f.write(f"{message.author} on {created}: {message.clean_content}\n")
                generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
                f.write(
                    f"\n*Generated at {generated} by {ctx.bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*\n*Credits: Made by rejectmodders on Discord!*")
            with open(f"{ctx.channel.id}.md", 'rb') as f:
                await ctx.send(file=discord.File(f, f"{ctx.channel.name}.md"))
            os.remove(f"{ctx.channel.id}.md")
        else:
            await ctx.send("This isn't a supported ticket channel!", ephemeral=True)

    @commands.hybrid_command(name='credits', description='Credits to who made the bot!')
    @commands.guild_only()
    async def credits(self, ctx):
        embed = discord.Embed(title="Ticket System Credits", description="This bot was created by RejectModders. Owner of UniBot, a Verified Discord Bot.", color=0x5865F2)

        embed.add_field(name="Server", value="[Support Server](https://discord.gg/nEyYXTnpEw)", inline=False)
        embed.add_field(name="Website", value="[Website](https://uni-bot.xyz/)", inline=False)
        embed.add_field(name="Invite",value="[Invite UniBot](https://discord.com/application-directory/1156134562418663585)", inline=False)

        await ctx.send(embed=embed)











