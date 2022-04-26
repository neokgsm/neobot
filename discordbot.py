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

# autorole
@bot.event
async def on_member_join(member):
    server = member.guild
    role = discord.utils.get(server.roles, name='Member')
    await member.add_roles(role)
    in_out = bot.get_channel(941963844807446529)
    await in_out.send(f'**[IN]** {member} joined.')

@bot.event
async def on_member_remove(member):
    in_out = bot.get_channel(941963844807446529)
    await in_out.send(f'**[OUT]** {member} left.')

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

# illegal word generator
n_list = ["n", "ń", "ñ"]
i_list = ["i", "ì", "į", "ī", "í", "ï", "î", "l", "1"]
e_list = ["e", "è", "é", "ê", "ë", "ē", "ė", "ę", "3"]
# s_list = ["", "s", "ś", "ś"]
illegal_words = []
for n in n_list:
    for i in i_list:
        for e in e_list:
            illegal_words.append(f'{n}{i}gg{e}r')

# 1984
@bot.event
async def on_message(message):
    if any(word in message.content.lower() for word in illegal_words):
        await message.delete()
    else:
        await bot.process_commands(message)

# ban cmd
@bot.command(name="ban")
async def ban(ctx, user="", reason=""):
    if user == '':
        await ctx.send('Missing user argument. Usage: $ban <user> <reason>')
    if reason == '':
        await ctx.send('Missing reason argument. Usage: $ban <user> <reason>')
    else:
        the_user = bot.get_user(int(user[3:-1]))
        reason = discord.utils.escape_mentions(reason)
        ban_txt = f'{ctx.author.mention} ({ctx.author} - {ctx.author.id}) banned {the_user.mention} ({str(the_user)} - {user[3:-1]}) for reason: {reason}'
        await ctx.send(ban_txt)
        mod_act = bot.get_channel(938112717892501545)
        await mod_act.send(ban_txt)

# sub
@bot.command()
async def sub(ctx):
    server = ctx.author.guild
    role = discord.utils.get(server.roles, name='Bajs')
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
    else:
        await ctx.author.add_roles(role)

# Nitro Boost
@bot.command()
async def boost(ctx):
    server = ctx.author.guild
    role = discord.utils.get(server.roles, name='Nitro Booster')
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
    else:
        await ctx.author.add_roles(role)

# nitro color
@bot.command()
async def color(ctx, nitro_color=""):
    server = ctx.author.guild
    the_role = discord.utils.get(server.roles, name=nitro_color)
    booster = discord.utils.get(server.roles, name='Nitro Booster')
    nitro_colors = [nc for nc in server.roles if 'nitro:' in nc.name]
    color_names = [nc.name for nc in server.roles if 'nitro' in nc.name]
    if nitro_color == "":
        await ctx.send("You need to provide a color. Usage: $color <colorname>")
    elif nitro_color not in color_names:
        await ctx.send("The specified color doesn't exist. Use $colors to see what colors are available")
    else:
        nitro_colors = [nc for nc in nitro_colors if nc != the_role]
        if the_role in ctx.author.roles:
            await ctx.author.remove_roles(the_role)
        else:
            for role in nitro_colors:
                if role in ctx.author.roles:
                    await ctx.author.remove_roles(role)
            await ctx.author.add_roles(the_role)
            await ctx.author.add_roles(booster)
            await ctx.send(f"Color {nitro_color} assigned correctly.")

# colors
@bot.command()
async def colors(ctx):
    server = ctx.author.guild
    color_names = [nc.name for nc in server.roles if 'nitro' in nc.name][::-1]
    txt = str(color_names).replace("'", "").replace(",", "")
    await ctx.send(f'These are the available colors: {txt}')

# accountage
@bot.command()
async def accountage(ctx):
    date = str(ctx.author.created_at)
    await ctx.send(f'{ctx.author.mention}, your account was created at {date[0:-7]} UTC')

# pfp
@bot.command()
async def pfp(ctx, id: int):
    user = await bot.fetch_user(id)
    url = user.avatar_url
    await ctx.send(url)

# test
@bot.command()
async def test(ctx):
    await ctx.send(f'{ctx.author.mention}, hi.')

bot.run(os.environ['DISCORD_BOT_TOKEN'])
