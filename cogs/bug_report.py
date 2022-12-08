#@Scarriana#5999
#December 2022
#Monumenta Discord Task Bot Prototype: bug report cog
import config
import discord
from discord import app_commands
from discord.ext import commands


class Bug_Report(commands.Cog):

	def __init__(self, bot: commands.Bot):
		self.bot = bot


	#sync bot: this is necessary, but also needs more than what I have now
	@commands.command()
	async def sync_report(self, ctx) -> None:
		fmt = await ctx.bot.tree.sync(guild=ctx.guild)
		await ctx.send(f'Synced{len(fmt)} commands.')
	
	#on ready
	@commands.Cog.listener()
	async def on_ready(self):

		print('Bug Report cog loaded.')

	#bug report form
	@app_commands.command(name="bugreport", description="bug report form")

	async def bugreport(self, interaction: discord.Interaction, tag: str, tag2: str):
		print(str)
		await interaction.response.send_message(f'Recieved: {str}')


#setting up cog for the bot: will need to adjust for which discord servers get passed into guilds
async def setup(bot):
		await bot.add_cog(Bug_Report(bot), guilds=[discord.Object(id=config.GUILD_ID)])
