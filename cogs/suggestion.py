#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: suggestion cog

import discord
from discord.ext import commands
from discord import ui, app_commands
import config
import traceback



class Suggestion(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	@commands.command()
	#sync bot: this is necessary, but also needs more than what I have now
	async def sync_suggestion(self, ctx) -> None:
		await ctx.send('Syncing command recieved')
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced {len(fmt)} commands in suggestion.py')
	
	@commands.Cog.listener()
	async def on_ready(self):
		print('Suggestion cog loaded.')


	@app_commands.command(name='suggestion', description='Enter a suggestion of how to improve the game. Bugs should be sent as a bug report.')
	@app_commands.describe(label='labels to choose from:')
	@app_commands.choices(label=[
        discord.app_commands.Choice(name='misc', value=1),
        discord.app_commands.Choice(name='advancement', value=2),
        discord.app_commands.Choice(name='boss', value=3),
        discord.app_commands.Choice(name='build', value=4),
        discord.app_commands.Choice(name='class', value=5),
        discord.app_commands.Choice(name='cmd', value=6),
        discord.app_commands.Choice(name='delve', value=7),
        discord.app_commands.Choice(name='depths', value=8),
        discord.app_commands.Choice(name='discord', value=9),
        discord.app_commands.Choice(name='enchantment', value=10),
        discord.app_commands.Choice(name='gui', value=11),
        discord.app_commands.Choice(name='item', value=12),
        discord.app_commands.Choice(name='mob', value=13),
        discord.app_commands.Choice(name='npc', value=14),
        discord.app_commands.Choice(name='plugin', value=15),
        discord.app_commands.Choice(name='quest', value=16),
        discord.app_commands.Choice(name='server', value=17),
        discord.app_commands.Choice(name='website', value=18),
        ])
	async def bugreport(self, interaction: discord.Interaction, 
		label: discord.app_commands.Choice[int], description: str):

		embed = discord.Embed(title = 'Suggestion', 
			description= label.name + "\n" + description, 
			color = discord.Color.yellow())

		# print("about to send the embed")
		await interaction.response.send_message(embed=embed)


		#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
	await bot.add_cog(Suggestion(bot), guilds=[discord.Object(id=config.GUILD_ID)])

