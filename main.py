import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  
bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Bot is online! Logged in as {bot.user}") 

@bot.command()
async def hello(ctx):
    await ctx.send(f"Hello there, {ctx.author.mention}!")  

@bot.command(aliases=["gm", "morning"])
async def goodmorning(ctx):
    await ctx.send(f"Good morning, {ctx.author.mention}!")

with open("token.txt", "r") as f:
    token = f.read().strip() 

bot.run(token)
