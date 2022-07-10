import discord
from discord.commands import slash_command
from discord.ext import commands, tasks
from dotenv import find_dotenv, load_dotenv
from os import getenv

from other_files import sync as sync_command
from other_files import auto_raid

__version__ = '0.0.1a'

intents = discord.Intents.default()
intents.members = True
bot = discord.Bot(debug_guilds=[739630717159473192,792217056644694057],intents=intents)

# loads the environment variables from .env
load_dotenv(find_dotenv())

# bot events
@bot.event
async def on_ready():
    print("Logged in as {0.user}".format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(f"EzAR V{__version__}"))

@bot.event
async def on_member_join(member):
    ar =  auto_raid.raidChecker(member)
    await ar.raidcheck()

@bot.event
async def on_member_remove(member):
    ...

# bot commands
@bot.slash_command()
async def ping(ctx):  # Passing a default value makes the argument optional
    """Get bot ping and basic info"""
    await ctx.respond(f"EzAntiRaid V{__version__}: ({round((bot.latency * 1000))}ms)")

@bot.slash_command()
async def sync(ctx):
    await sync_command.sync(ctx)

# tasks
@tasks.loop(hours=24.0) #this task will upload the database as a backup every 24 hours
async def upload_db():
    global bot
    db = bot.get_channel(972541376375975996)
    await db.send(file=discord.File('ezantiraid.json'))
@upload_db.before_loop
async def before_upload_db():
    global bot
    await bot.wait_until_ready()


#start tasks
upload_db.start()

# run bot
bot.run(getenv('bot_key'))