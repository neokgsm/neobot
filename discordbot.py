import discord
from discord.ext import commands
import os
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='$', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')

@bot.group()
async def cool(ctx):
    """Says if a user is cool.
    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'No, {ctx.subcommand_passed} is not cool')

@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')

# 8ball
@bot.command(name="8ball")
async def _8ball(ctx):
    ans = ["It is certain.",
           "It is decidedly so.",
           "Without a doubt.",
           "Yes definitely.",
           "You may rely on it.",
           "As I see it, yes.",
           "Most likely.",
           "Outlook good.",
           "Yes.",
           "Signs point to yes.",
           "Reply hazy try again.",
           "Ask again later.",
           "Better not tell you now.",
           "Cannot predict now.",
           "Concentrate and ask again.",
           "Don't count on it.",
           "My reply is no.",
           "My sources say no.",
           "Outlook not so good.",
           "Very doubtful."]
    await ctx.send(f'{ctx.author.mention}, {ans[random.randrange(len(ans))]}')

# ping
@bot.command()
async def ping(ctx):
    ans = ["pang", "ping", "pung", "peng", "pong"]
    await ctx.send(f'{ctx.author.mention}, {ans[random.randrange(len(ans))]}.')

# 1984
illegal_words = ["nigger"]
@bot.event
async def on_message(message):
    if any(word in message.content for word in illegal_words):
        await message.delete()
    else:
        await bot.process_commands(message)

# ban
@bot.command(name="ban")
async def ban(ctx, user="", reason=""):
    if user == '':
        await ctx.send('Missing user argument. Usage: $ban <user> <reason>')
    if reason == '':
        await ctx.send('Missing reason argument. Usage: $ban <user> <reason>')
    else:
        the_user = bot.get_user(int(user[3:-1]))
        await ctx.send(f'{ctx.author.mention} ({ctx.author} - {ctx.author.id}) banned {the_user.mention} ({str(the_user)} - {user[3:-1]}) for reason: {reason}')

# test
@bot.command()
async def test(ctx):
    await ctx.send(f'{ctx.author.mention}, hi.')

bot.run(os.environ['DISCORD_BOT_TOKEN'])
