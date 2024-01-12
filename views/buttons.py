import discord, os, config
from datetime import datetime
from discord import app_commands, utils
from discord.ext import commands


class ticket_launcher(discord.ui.View):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(timeout=None)
        self.cooldown = commands.CooldownMapping.from_cooldown(1, 600, commands.BucketType.member)
        self.bot = bot

    @discord.ui.button(label="• Support", emoji='👷', style=discord.ButtonStyle.blurple, custom_id="support")
    async def ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user

        ticket_category_name = "Support Tickets"
        ticket_category = utils.get(interaction.guild.categories, name=ticket_category_name)

        if ticket_category is None:
            return await interaction.response.send_message(f"Ticket category '{ticket_category_name}' not found!",
                                                           ephemeral=True)

        ticket_channel_name = f"{interaction.user.name.lower().replace(' ', '-')}-support-ticket"
        ticket = utils.get(ticket_category.text_channels, name=ticket_channel_name)

        if ticket is not None:
            return await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!",
                                                           ephemeral=True)

        if type(self.bot.ticket_mod) is not discord.Role:
            self.bot.ticket_mod = interaction.guild.get_role(roleid)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                          send_messages=True, attach_files=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                              read_message_history=True),
            self.bot.ticket_mod: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                        send_messages=True, attach_files=True, embed_links=True),
        }

        try:
            channel = await interaction.guild.create_text_channel(
                name=ticket_channel_name, category=ticket_category, overwrites=overwrites,
                reason=f"Ticket for {interaction.user}")
        except Exception as e:
            print(f"Error creating channel: {e}")
            return await interaction.response.send_message(
                "Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral=True)

        embed = discord.Embed(
            title="Support Ticket Created",
            description="- This is a **👷 • Support Ticket**. If you accidentally opened the wrong ticket, please close it and open the correct one.\n\n"
                        "- While you wait for staff assistance, please describe the issue you are experiencing. Providing details in advance will help our staff assist you more efficiently.\n\n"
                        "- To close this ticket, please react with 🔒.",
            color=config.main_color
        )

        await channel.send(embed=embed, view=main(self.bot))
        await interaction.response.defer()
        await interaction.followup.send(f"I've opened a ticket for you at {channel.mention}!", ephemeral=True)

    @discord.ui.button(label="• Apply For Staff", emoji='✅', style=discord.ButtonStyle.blurple, custom_id="staff")
    async def staff_application_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user

        ticket_category_name = "Apply For Staff Tickets"
        ticket_category = utils.get(interaction.guild.categories, name=ticket_category_name)

        if ticket_category is None:
            return await interaction.response.send_message(f"Ticket category '{ticket_category_name}' not found!",
                                                           ephemeral=True)

        ticket_channel_name = f"{interaction.user.name.lower().replace(' ', '-')}-staff-application-ticket"
        ticket = utils.get(ticket_category.text_channels, name=ticket_channel_name)

        if ticket is not None:
            return await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!",
                                                           ephemeral=True)

        if type(self.bot.ticket_mod) is not discord.Role:
            self.bot.ticket_mod = interaction.guild.get_role(roleid)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                          send_messages=True, attach_files=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                              read_message_history=True),
            self.bot.ticket_mod: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                        send_messages=True, attach_files=True, embed_links=True),
        }

        try:
            channel = await interaction.guild.create_text_channel(
                name=ticket_channel_name, category=ticket_category, overwrites=overwrites,
                reason=f"Ticket for {interaction.user}")
        except:
            return await interaction.response.send_message(
                "Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral=True)

        embed = discord.Embed(
            title="Apply For Staff Ticket Created",
            description="- This is a **✅ • Apply For Staff Ticket**. If you accidentally opened the wrong ticket, please close it and open the correct one.\n\n"
                        "- To join our staff, kindly complete this [form](https://forms.gle/51BYb4DKozGVnXmf6). Once you've filled out the form, please reply with `Done` in the ticket so we can acknowledge your completion. If there's no response within 12 hours, we may close the ticket, so please inform us promptly if you're done!\n\n"
                        "- To close this ticket, please react with 🔒.",
            color=config.main_color
        )
        await channel.send(embed=embed, view=main(self.bot))
        await interaction.response.defer()
        await interaction.followup.send(f"I've opened a ticket for you at {channel.mention}!", ephemeral=True)

    @discord.ui.button(label="• Report User", emoji='🚨', style=discord.ButtonStyle.blurple, custom_id="report")
    async def report_user_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        interaction.message.author = interaction.user

        ticket_category_name = "Report Tickets"
        ticket_category = utils.get(interaction.guild.categories, name=ticket_category_name)

        if ticket_category is None:
            return await interaction.response.send_message(f"Ticket category '{ticket_category_name}' not found!",
                                                           ephemeral=True)

        ticket_channel_name = f"{interaction.user.name.lower().replace(' ', '-')}-report-user-ticket"
        ticket = utils.get(ticket_category.text_channels, name=ticket_channel_name)

        if ticket is not None:
            return await interaction.response.send_message(f"You already have a ticket open at {ticket.mention}!",
                                                           ephemeral=True)

        if type(self.bot.ticket_mod) is not discord.Role:
            self.bot.ticket_mod = interaction.guild.get_role(roleid)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                          send_messages=True, attach_files=True, embed_links=True),
            interaction.guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                              read_message_history=True),
            self.bot.ticket_mod: discord.PermissionOverwrite(view_channel=True, read_message_history=True,
                                                        send_messages=True, attach_files=True, embed_links=True),
        }

        try:
            channel = await interaction.guild.create_text_channel(
                name=ticket_channel_name, category=ticket_category, overwrites=overwrites,
                reason=f"Ticket for {interaction.user}")
        except:
            return await interaction.response.send_message(
                "Ticket creation failed! Make sure I have `manage_channels` permissions!", ephemeral=True)

        embed = discord.Embed(
            title="Report User Ticket Created",
            description="- This is a **🚨 • Report User Ticket**. If you accidentally opened the wrong ticket, please close it and open the correct one.\n\n"
                        "- While you wait for staff to review your report, please provide all relevant details and evidence regarding the issue or user you're reporting. This will assist our staff in conducting a thorough investigation.\n\n"
                        "- To close this ticket, please react with 🔒.",
            color=config.main_color
        )

        await channel.send(embed=embed, view=main(self.bot))
        await interaction.response.defer()
        await interaction.followup.send(f"I've opened a ticket for you at {channel.mention}!", ephemeral=True)


class confirm(discord.ui.View):
    def __init__(self, ticket_channel, transcript_channel_id, bot: commands.Bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot
        self.ticket_channel = ticket_channel
        self.transcript_channel_id = transcript_channel_id

    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.red, custom_id="confirm")
    async def confirm_button(self, interaction, button):
        if os.path.exists(f"{self.ticket_channel.id}.md"):
            await interaction.followup.send(f"A transcript is already being generated!", ephemeral=True)
            return

        with open(f"{self.ticket_channel.id}.md", 'a') as f:
            f.write(f"# Transcript of {self.ticket_channel.name}:\n\n")
            async for message in self.ticket_channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {self.bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")

        transcript_channel = self.bot.get_channel(self.transcript_channel_id)
        if transcript_channel:
            with open(f"{self.ticket_channel.id}.md", 'rb') as f:
                await transcript_channel.send(file=discord.File(f, f"{self.ticket_channel.name}.md"))
            os.remove(f"{self.ticket_channel.id}.md")
        else:
            await interaction.followup.send("Transcript channel not found! Please configure it.", ephemeral=True)

        try:
            await self.ticket_channel.delete()
        except:
            await interaction.followup.send("Channel deletion failed! Make sure I have `manage_channels` permissions!", ephemeral=True)


class main(discord.ui.View):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__(timeout=None)
        self.bot = bot

    @discord.ui.button(label="Close Ticket", emoji='🔒', style=discord.ButtonStyle.red, custom_id="close")
    async def close(self, interaction, button):
        allowed_role_id = roleid

        user = interaction.user
        allowed_role = interaction.guild.get_role(allowed_role_id)

        if allowed_role and allowed_role in user.roles:
            embed = discord.Embed(title="Are you sure you want to close this ticket?", color=discord.Colour.blurple())

            ticket_channel = interaction.channel
            transcript_channel_id = channelid

            await interaction.response.send_message(embed=embed, view=confirm(ticket_channel, transcript_channel_id, self.bot), ephemeral=True)
        else:
            await interaction.response.send_message("Only Staff can close the ticket! ", ephemeral=True)


    @discord.ui.button(label="Transcript", style=discord.ButtonStyle.blurple, custom_id="transcript")
    async def transcript(self, interaction, button):
        await interaction.response.defer()
        if os.path.exists(f"{interaction.channel.id}.md"):
            return await interaction.followup.send(f"A transcript is already being generated!", ephemeral=True)
        with open(f"{interaction.channel.id}.md", 'a') as f:
            f.write(f"# Transcript of {interaction.channel.name}:\n\n")
            async for message in interaction.channel.history(limit=None, oldest_first=True):
                created = datetime.strftime(message.created_at, "%m/%d/%Y at %H:%M:%S")
                if message.edited_at:
                    edited = datetime.strftime(message.edited_at, "%m/%d/%Y at %H:%M:%S")
                    f.write(f"{message.author} on {created}: {message.clean_content} (Edited at {edited})\n")
                else:
                    f.write(f"{message.author} on {created}: {message.clean_content}\n")
            generated = datetime.now().strftime("%m/%d/%Y at %H:%M:%S")
            f.write(f"\n*Generated at {generated} by {self.bot.user}*\n*Date Formatting: MM/DD/YY*\n*Time Zone: UTC*")
        with open(f"{interaction.channel.id}.md", 'rb') as f:
            await interaction.followup.send(file=discord.File(f, f"{interaction.channel.name}.md"))
        os.remove(f"{interaction.channel.id}.md")
