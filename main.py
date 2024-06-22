import nextcord
from nextcord import Interaction
from nextcord.ext import commands
import random


intents = nextcord.Intents.default()
intents.members = True  


client = commands.client(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("The client is now ready for use!")
    print("...")  

test_server_id = ###############


responses = [
  "It is certain.",
  "It is decidedly so.",
  "Ask again later.",
  "Cannot predict now.",
  "Do not count on it.",
  "My sources are unclear.",
  "Outlook not so good.",
  "Very doubtful."
]


@client.slash_command(name="coinflip", description="Flip a coin")
async def coinflip(interaction: nextcord.Interaction):
  flip = random.randint(0, 1)
  if flip == 0:
    await interaction.response.send_message("Heads!")
  else:
    await interaction.response.send_message("Tails!")

@client.slash_command(name="8ball", description="Ask the magic 8 ball a question.")
async def eight_ball(interaction: nextcord.Interaction, question: str):
  if question == "":
    await interaction.response.send_message("Please ask a question.")
  else:
    answer = random.choice(responses)
    await interaction.response.send_message(f"{question}\n{answer}")



@client.slash_command(
    name="test",
    description="Introduction to Slash Commands",
    guild_ids=[test_server_id]  
)
async def test(interaction: Interaction):
    await interaction.response.send_message("Hello, subscribe please :)")

client.run(client_TOKEN)
