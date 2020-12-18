import discord
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

	class ConvertIntCommand(commands.Command):
		async def do_conversion(self, ctx, converter, argument, param):
			if isinstance(argument, str):
				argument = argument.replace(',', '')
			return await super().do_conversion(ctx, converter, argument, param)

	@commands.command(cls=ConvertIntCommand)
	# TODO: Add limitations on who can use
	# this command as we wouldn't want people
	# adding XP to themselves
	async def givexp(self, ctx, amount: int, receiver=commands.UserConverter()):
		if not isinstance(receiver, discord.User):
			receiver = ctx.author
		user = await self.session.run_sync(UserXP.get_or_create, receiver.id)
		user.xp += amount
		await self.session.commit()
		await ctx.send(f"{ctx.author.mention} You have succesfully added {amount:,} XP "
					   f"to {'yourself' if receiver == ctx.author else receiver.mention}!")

	@givexp.error
	async def handle_givexp_error(self, ctx, error):
		if isinstance(error, commands.MissingRequiredArgument):
			await ctx.send(f"{ctx.author.mention} You must provide an amount of XP to add.")
		elif isinstance(error, commands.UserNotFound):
			await ctx.send(f"{ctx.author.mention} `{ctx.message.content.split()[2]}` is not a valid user!")
		elif isinstance(error, commands.BadArgument):
			await ctx.send(f"{ctx.author.mention} `{ctx.message.content.split()[1]}` is not a valid amount of XP.")
		else:
			await ctx.send(f"{ctx.author.mention} Congrats, you managed to break the "
						   f"`{ctx.prefix}givexp` command!")
