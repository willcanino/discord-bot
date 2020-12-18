import discord
from discord.ext import commands
from bot.tables import Base as base, UserXP
from bot.commands import Commands
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

class bot(commands.Bot):
	def __init__(self, *args, uri='sqlite:///:memory:', **kwargs):
		self.engine = create_async_engine(uri)
		self.session = AsyncSession(bind=self.engine)
		super().__init__(*args, **kwargs)
		self.add_cog(Commands(self.engine, self))

	async def on_connect(self):
		async with self.engine.begin() as conn:
			await conn.run_sync(base.metadata.create_all)

	async def on_message(self, message):
		if not message.author.bot:
			def add_user(session):
				user = session.query(UserXP).filter(UserXP.discord_id == message.author.id) \
					   .one_or_none()
				if user is None:
					user = UserXP(discord_id=message.author.id, xp=0)
					session.add(user)
				user.xp += 1
			await self.session.run_sync(add_user)
			await self.session.commit()

		await self.process_commands(message)
