import discord, asyncio, time, config
from discord.ext import commands, tasks
import datetime
from views.buttons import ticket_launcher, confirm


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.reactions = True
        intents.typing = False
        intents.presences = True
        intents.guilds = True
        intents.invites = True
        self.ticket_mod = 1174258310074081330

        super().__init__(command_prefix='!', intents=intents)


    async def setup_hook(self):
        """A function called when the bot logs in."""
        print(f'{self.user.name} has logged in successfully.')
        await self.load_extension('commands.cog_setup1')
        self.add_view(ticket_launcher(bot))
        print(f'Ticket Buttons added!')



bot = Bot()

async def run1():
    await bot.start(config.TOKEN)


@bot.listen()
async def on_ready():
    print(f'{bot.user.name} is ready to recieve commands.')

