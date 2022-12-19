#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype
#main.py: starts the bot and loads the cogs (contain commands for bug reports and suggestions)

import discord
#from discord import app_commands
from discord.ext import commands
# from discord import option
import config
import asyncio
import os
import json

intents = discord.Intents.default()
intents.message_content = True

# Client/Bot set up
class MyBot(commands.Bot):


    def __init__(self):
        super().__init__(
            command_prefix='.',
            intents = intents,
            application_id=config.APPLICATION_ID)

    async def setup_hook(self):
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                await self.load_extension(f'cogs.{file[:-3]}')

bot = MyBot()
print('made the bot')

@bot.event
async def on_ready():
    print('Online.')

@bot.event
async def on_message(message):
    await bot.process_commands(message)
    if message[0] == '.':
        print('.')
        return
    if message.author == bot.user:
        return
    await message.channel.send("got here")

async def main():
    await bot.start(config.TOKEN)

asyncio.run(main())

