import discord
from discord.ext import commands 

app = commands.Bot(command_prefix='!!',intents=discord.Intents.all())

@app.event
async def on_ready():
   print(f"[PconnMonitoring] Started")
   activity = discord.Activity(type=discord.ActivityType.listening,name='PconnMonitoring')
   await app.change_presence(status=discord.Status.online,activity=activity)

app.load_extension('Cogs.lookup')

app.run('token')
