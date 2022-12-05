#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype

import discord
from discord import app_commands
from discord.ext import commands
import config
import asyncio
import os

my_guild = discord.Object(config.GUILD_ID)

#Client set up
# class MyClient(discord.Client):
# 	def __init__(self, *args, **kwargs):
# 		super().__init__(*args, **kwargs)

# 	async def on_ready(self):
# 		await tree.sync(guild = my_guild)
# 		print('Online')

#come back to intents later: currently using admin perms in test server, want to change later
intents = discord.Intents.default()
intents.message_content = True

#fix this when ready to test the forms: 
bot = commands.Bot(command_prefix='.', intents=intents, application_id=config.APPLICATION_ID)



@bot.event
async def on_ready():
	print('Setting up . . . beep beep')


@bot.event
async def on_message(message):
	await bot.process_commands(message)
	('bot here')
	#ignore commands
	if message[0] == '.':
		print('.')
		return
	if message.author == bot.user:
		print('bot')
		return
	await message.channel.send('message seen')
#load all cogs from cogs folder
async def load():
	for file in os.listdir('./cogs'):
		if file.endswith('.py'):
			await bot.load_extension(f'cogs.{file[:-3]}')


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



#starts the bot
async def main():
	await load()
	# await load()
	# await client.start(config.TOKEN)
	await bot.start(config.TOKEN)


asyncio.run(main())