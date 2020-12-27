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
        if not message.author.bot and message.guild:
            user, commit = await self.session.run_sync(UserXP.get_or_create,
                                                       message.author.id,
                                                       message.guild.id,
                                                       commit=True)
            if commit: await self.session.commit()
            user.xp += 1

    @commands.command()
    @commands.guild_only()
    async def xp(self, ctx, person=commands.MemberConverter()):
        if not isinstance(person, discord.Member):
            person = ctx.author
        user, commit = await self.session.run_sync(UserXP.get_or_create,
                                                   person.id,
                                                   ctx.guild.id,
                                                   commit=True)
        if commit: await self.session.commit()
        # Need the plus 1 because on_message runs after
        # any command called
        if person == ctx.author:
            await ctx.send(f"{ctx.author.mention}, You currently have {user.xp + 1:,} XP!")
        else:
            await ctx.send(f"{ctx.author.mention}, {person.mention} currently has {user.xp + 1:,} XP!")
        # NOTE: User is added to database in on_message!
        # The user in this situation is not added
        # to the database until session.commit()
        # is called. This occurs in the on_message
        # method; something to keep in mind.

    @xp.error
    async def handle_xp_error(self, ctx, error):
        if isinstance(error, commands.NoPrivateMessage):
            await ctx.send('This command is not available in DMs. Try using it in a server with me')
        else:
            print(f'XP Command error: {repr(error)}')
            await ctx.send(f"Congrats, you managed to break the `{ctx.prefix}xp` command!")

    class ConvertIntCommand(commands.Command):
        async def do_conversion(self, ctx, converter, argument, param):
            if isinstance(argument, str):
                argument = argument.replace(',', '')
            return await super().do_conversion(ctx, converter, argument, param)

    @commands.command(cls=ConvertIntCommand)
    @commands.has_guild_permissions(administrator=True)
    async def givexp(self, ctx, amount: int, receiver=commands.MemberConverter()):
        if not isinstance(receiver, discord.Member):
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
            print(f"GiveXP command error: {error!r}")
            await ctx.send(f"{ctx.author.mention} Congrats, you managed to break the "
                           f"`{ctx.prefix}givexp` command!")

    #clear command/error vv
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(ctx, amount=5):
        await ctx.channel.purge(limit=amount)

    @clear.error
    async def clear_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} you cannot use this command! :cry:')

    #kick command/error vv
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(ctx, member: commands.MemberConverter(), *, reason=None):
        embed = discord.Embed(title=f'You Have Been Kicked From {ctx.guild}',
                            description=f'Reason for Kick: {reason}', colour=discord.Colour.from_rgb(67, 181, 129))
        embed.set_footer(icon_url=str(client.user.avatar_url),
                        text=f'WillCaninoBot Alpha • {datetime.date.today()}')
        await member.send(embed=embed)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} you don\'t have the correct role to use this command! :cry:')
        else:
            await ctx.send(f'Unknown error occured: {error!r}')

    #ban command/error vv
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: commands.MemberConverter(), *, reason=None):
        embed = discord.Embed(title=f'You Have Been Banned From {ctx.guild}',
                            description=f'Reason for Ban: {reason}', colour=discord.Colour.from_rgb(67, 181, 129))
        embed.set_footer(icon_url=str(client.user.avatar_url),
                        text=f'WillCaninoBot Alpha • {datetime.date.today()}')
        await member.send(embed=embed)
        await member.kick(reason=reason)

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send(f'{ctx.author.mention} you don\'t have the correct role to use this command! :cry:')
        else:
            await ctx.send(f'Unknown error occured: {error!r}')

    #unban command/error vv

    @commands.command()
    async def unban(ctx, *, member):
        banned_users = await ctx.quild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return

    @commands.command()
    @commands.guild_only()
    async def level(self, ctx, person=commands.MemberConverter()):
        if not isinstance(person, discord.Member):
            person = ctx.author
        user, commit = await self.session.run_sync(UserXP.get_or_create,
                                                   person.id,
                                                   ctx.guild.id,
                                                   commit=True)
        if commit: await self.session.commit()

        if person == ctx.author:
            # NOTE: Since the on_message listener
            # is run after commands are invoked
            # we have to manually increase the xp
            # since the xp does not account for the
            # message that was sent to invoke this
            # command
            user.xp += 1
            await ctx.send(f"{ctx.author.mention}, You are currently at level {user.level:,}!")
            user.xp -= 1
        else:
            await ctx.send(f"{ctx.author.mention}, {person.mention} is currently at level {user.level:,}")
