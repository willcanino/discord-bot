from sqlalchemy.ext.asyncio import AsyncSession
from discord.ext import commands

class Commands(commands.Cog):
	def __init__(self, engine, bot):
		self.engine = engine
		self.bot = bot
		self.session = AsyncSession(bind=self.engine)
