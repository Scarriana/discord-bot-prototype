#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype

import discord
#from discord import app_commands
from discord.ext import commands
# from discord import option
import config
import asyncio
import os

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



#my_guild = discord.Object(config.GUILD_ID)



# 		#starts the bot
# async def main():
# 	bot = MyBot()
# 	await bot.start(config.TOKEN)

# asyncio.run(main())

# @bot.event
# async def on_message(message):
# 	await bot.process_commands(message)
# 	('bot here')
# 	#ignore commands
# 	if message[0] == '.':
# 		print('.')
# 		return
# 	if message.author == bot.user:
# 		print('bot')
# 		return
# 	await message.channel.send('message seen')
#load all cogs from cogs folder



# client = MyClient(intents=intents)

#for app commands: use for NickNackGus's idea of pings?
# tree = app_commands.CommandTree(bot)
# @tree.context_menu(name="Help!", guild=my_guild)
# async def hello(interaction: discord.Interaction, message: discord.Message):
# 	channel = await interaction.user.create_dm()
# 	await channel.send('Insert generic help message here')
# 	#dms the user something
# 	await interaction.response.send_message('Help is on the way!')

#slash commands (as a cog):
# - create suggestions_form.py that contains the cog stuff needed
# - create bug_reports.py form that contains bug reports cog stuff
