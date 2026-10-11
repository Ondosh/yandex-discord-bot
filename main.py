import discord

from bot.core import Bot
from bot.cfg import token
import bot.interactions
import bot.music


@Bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.custom, name='$ - prefix')
    await Bot.change_presence(status=discord.Status.online, activity=activity)
    print("Бот запущен!")

Bot.run(token)
