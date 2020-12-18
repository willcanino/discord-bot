from bot import discord_bot

the_bot = discord_bot(command_prefix='test.')

the_bot.run(open('token.txt').read().strip('\n'))
