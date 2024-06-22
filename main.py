import discord
from discord.ext import commands

intents = discord.Intents.default()  

bot = commands.Bot(command_prefix=".", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")

@bot.command()
async def sendembed(ctx):
    embed = discord.Embed(
        title="Title of embed",
        description="Description of embed",
        color=discord.Color.green()
    )
    embed.set_author(name="Footer text", icon_url=ctx.author.avatar.url)
    embed.set_thumbnail(url=ctx.author.avatar.url)
    embed.add_field(name="Name of field", value="Value of field", inline=False)
    embed.set_image(url=ctx.guild.icon.url)
    embed.set_footer(text="Footer text", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=embed)

@bot.command()
async def ping(ctx):
    ping_embed = discord.Embed(
        title="Ping",
        description="Latency in ms",
        color=discord.Color.blue()
    )
    ping_embed.add_field(
        name=f"{bot.user.name}'s Latency (ms):",
        value=f"{round(bot.latency * 1000)}ms",
        inline=False
    )
    ping_embed.set_footer(text=f"Requested by {ctx.author.name}.", icon_url=ctx.author.avatar.url)
    await ctx.send(embed=ping_embed)





with open("token.txt", "r") as f:
    token = f.read().strip() 

bot.run(token)
