import discord
from discord.ext import commands


class PersistentViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default() # guilds и voice_states, без привилегированных intents
        super().__init__(intents=intents, command_prefix="$", help_command=None)


    async def setup_hook(self):
        await self.tree.sync()