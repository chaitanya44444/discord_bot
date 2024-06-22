import discord
from discord.ext import commands
import asyncio  

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix=".", intents=intents)

afk_status = {}

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def afk(ctx, reason=""):
    afk_status[ctx.author.id] = reason
    await ctx.channel.send(f"{ctx.author.mention} is now afk. {(reason if reason else '')}")

@bot.command()
async def backfromafk(ctx):
    if ctx.author.id in afk_status:
        del afk_status[ctx.author.id]
        await ctx.channel.send(f"{ctx.author.mention} is back from afk.")
    else:
        await ctx.channel.send(f"{ctx.author.mention} is not currently afk.")

@bot.command()
async def emoji(ctx, emoji_name):
    try:
        custom_emoji = discord.utils.get(ctx.guild.emojis, name=emoji_name)
        if custom_emoji:
            await ctx.send(custom_emoji.url)
            return

        unicode_emoji = discord.utils.get(discord.emojis, name=emoji_name)
        if unicode_emoji:
            await ctx.send(f"https://snyk.io/advisor/python/emoji/functions/emoji.UNICODE_EMOJI.items") 
            return

        await ctx.send(f"Emoji '{emoji_name}' not found.")
    except discord.HTTPException:
        await ctx.send("Failed to retrieve emoji. Please check the emoji name.")

@bot.event
async def on_member_join(member):
    
    if member.id in afk_status:
        del afk_status[member.id]
        await member.guild.default_channel.send(f"{member.mention} is back from afk and the void like tf.")

@bot.event
async def on_message(message):
    
    if message.author.id in afk_status and message.author != bot.user:
        del afk_status[message.author.id]
        await message.channel.send(f"{message.author.mention} is back from afk. {(afk_status.get(message.author.id) if afk_status.get(message.author.id) else '')}")
    await bot.process_commands(message)  s

token = os.environ.get('BOT_TOKEN')  

bot.run(token)
