from discord.ext import commands
from bot.tables import UserXP
from sqlalchemy.ext.asyncio import AsyncSession

class Commands(commands.Cog):
	def __init__(self, engine, bot):
		self.engine = engine
		self.bot = bot
		self.session = AsyncSession(bind=self.engine)

	@commands.command()
	async def xp(self, ctx, *message):
		def get_user(session):
			return session.query(UserXP).filter(UserXP.discord_id == ctx.author.id).one()
		user = await self.session.run_sync(get_user)
		await ctx.send(f"{ctx.author.mention} You currently have {user.xp} XP!")
