import discord
from discord.ext import commands
from bot.tables import Base as base, UserXP
from sqlalchemy.ext.asyncio import create_async_engine

class bot(commands.Bot):
	def __init__(self, *args, uri='sqlite:///:memory:', **kwargs):
		self.engine = create_async_engine(uri)
		super().__init__(*args, **kwargs)

	async def on_connect(self):
		async with self.engine.begin() as conn:
			await conn.run_sync(base.metadata.create_all)
