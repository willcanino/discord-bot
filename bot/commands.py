import discord
from discord.ext import commands
from bot.tables import UserXP
from sqlalchemy.ext.asyncio import AsyncSession

class Commands(commands.Cog):
    def __init__(self, engine, bot):
        self.engine = engine
        self.bot = bot
        self.session = AsyncSession(bind=self.engine)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            user, commit = await self.session.run_sync(UserXP.get_or_create,
                                                       message.author.id,
                                                       message.guild.id,
                                                       commit=True)
            if commit: await self.session.commit()
            user.xp += 1

    @commands.command()
    async def xp(self, ctx, *message):
        user, commit = await self.session.run_sync(UserXP.get_or_create,
                                                   ctx.author.id,
                                                   ctx.guild.id,
                                                   commit=True)
        if commit: await self.session.commit()
        # Need the plus 1 because on_message runs after
        # any command called
        await ctx.send(f"{ctx.author.mention} You currently have {user.xp + 1:,} XP!")
        # NOTE: User is added to database in on_message!
        # The user in this situation is not added
        # to the database until session.commit()
        # is called. This occurs in the on_message
        # method; something to keep in mind.

    class ConvertIntCommand(commands.Command):
        async def do_conversion(self, ctx, converter, argument, param):
            if isinstance(argument, str):
                argument = argument.replace(',', '')
            return await super().do_conversion(ctx, converter, argument, param)

    @commands.command(cls=ConvertIntCommand)
    @commands.has_guild_permissions(administrator=True)
    async def givexp(self, ctx, amount: int, receiver=commands.UserConverter()):
        if not isinstance(receiver, discord.User):
            receiver = ctx.author
        user = await self.session.run_sync(UserXP.get_or_create, receiver.id, ctx.guild.id)
        user.xp += amount
        await self.session.commit()
        await ctx.send(f"{ctx.author.mention} You have succesfully given {amount:,} XP "
                       f"to {'yourself' if receiver == ctx.author else receiver.mention}!")

    @givexp.error
    async def handle_givexp_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"{ctx.author.mention} You must provide an amount of XP to add.")
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(f"{ctx.author.mention} `{ctx.message.content.split()[2]}` is not a valid user!")
        elif isinstance(error, commands.BadArgument):
            await ctx.send(f"{ctx.author.mention} `{ctx.message.content.split()[1]}` is not a valid amount of XP.")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send((f"{ctx.author.mention} You do not have the required permissions to use the "
                            f"`{ctx.prefix}givexp` command. "
                            "You must have a role that has the 'admin' permission."))
        elif isinstance(error, commands.NoPrivateMessage):
            await ctx.send(f"The `{ctx.prefix}givexp` command is unavailable in DMs. "
                            "Please try using it in a server.")
        else:
            await ctx.send(f"{ctx.author.mention} Congrats, you managed to break the "
                           f"`{ctx.prefix}givexp` command!")
