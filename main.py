import nextcord
from nextcord import Interaction
from nextcord.ext import commands

intents = nextcord.Intents.default()
intents.members = True  


client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready for use!")
    print("...")  

test_server_id = ###############

@client.slash_command(
    name="test",
    description="Introduction to Slash Commands",
    guild_ids=[test_server_id]  
)
async def test(interaction: Interaction):
    await interaction.response.send_message("Hello, subscribe please :)")

client.run(BOT_TOKEN)
