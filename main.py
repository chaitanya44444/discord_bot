import nextcord
from nextcord import Interaction, SelectOption
from nextcord.ext import commands
from nextcord.ui import Select, View
import requests, csv
import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_SERVER_ID = 1128015206564503613

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True  

client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    print("The bot is now ready for use!")

@client.slash_command(name="quote", description="Get a random inspirational quote.")
async def quote(interaction: nextcord.Interaction):
    url = "https://api.forismatic.com/api/1.0/?method=getQuote&lang=en&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        quote_data = response.json()
        quote = quote_data["quoteText"]
        author = quote_data["quoteAuthor"]
        await interaction.response.send_message(f"{quote}\n- {author}")
    else:
        await interaction.response.send_message("Error getting quote. Please try again later.")

@client.slash_command(
    name="test",
    description="Introduction to Slash Commands",
    guild_ids=[YOUR_SERVER_ID]  
)
async def test(interaction: Interaction):
    await interaction.response.send_message("Hello, subscribe please :)")

@client.event
async def on_message_delete(message):
    if not message.guild or not message.content:
        return
    guild_id = str(message.guild.id)
    channel_id = str(message.channel.id)
    file_path = f"snipe_{guild_id}_{channel_id}.csv"

    try:
        with open(file_path, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([message.author.name, message.content])
    except FileNotFoundError:
        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Author", "Message"])
            writer.writerow([message.author.name, message.content])

class SnipeSelect(Select):
    def __init__(self, options):
        super().__init__(
            placeholder="Choose number of messages to snipe",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: nextcord.Interaction):
        num = int(self.values[0])
        guild_id = str(interaction.guild.id)
        channel_id = str(interaction.channel.id)
        file_path = f"snipe_{guild_id}_{channel_id}.csv"

        try:
            with open(file_path, mode='r') as file:
                reader = csv.reader(file)
                messages = list(reader)[1:]  # Skip header row
                if len(messages) == 0:
                    await interaction.response.send_message("There are no messages to snipe.")
                    return
                elif num > len(messages):
                    num = len(messages)
                snipe_messages = messages[-num:] 
                snipe_str = "\n".join(f'{message[0]}: {message[1]}' for message in snipe_messages)
                await interaction.response.send_message(f'Deleted message(s) {num}:\n{snipe_str}')
        except FileNotFoundError:
            await interaction.response.send_message("There are no messages to snipe.")

@client.slash_command(name="snipe", description="Snipes a deleted message (or multiple).", guild_ids=[YOUR_SERVER_ID])
async def snipe(interaction: nextcord.Interaction):
    guild_id = str(interaction.guild.id)
    channel_id = str(interaction.channel.id)
    file_path = f"snipe_{guild_id}_{channel_id}.csv"

    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            messages = list(reader)[1:]  
            if len(messages) == 0:
                await interaction.response.send_message("There are no messages to snipe.")
                return

            num_messages = min(15, len(messages))  
            options = [SelectOption(label=f"{i}", value=f"{i}") for i in range(1, num_messages + 1)]
            view = View()
            view.add_item(SnipeSelect(options))
            await interaction.response.send_message("Select the number of messages to snipe:", view=view, ephemeral=True)
    except FileNotFoundError:
        await interaction.response.send_message("There are no messages to snipe.")

@client.slash_command(name="rickroll", description="Rickroll a user via DM.")
async def rickroll(interaction: nextcord.Interaction, user: nextcord.User):
    rickroll_url = "https://tenor.com/view/when-you-get-rickrolled-by-funguyalt-22954713"
    rickrolled_by = interaction.user.mention
    rickrolled_user = user.mention

    try:
        await user.send(f"{rickrolled_user}, you were rickrolled by {rickrolled_by}!\n{rickroll_url}")
        await interaction.response.send_message(f"Successfully rickrolled {rickrolled_user}!")
    except nextcord.HTTPException:
        await interaction.response.send_message(f"Failed to send DM to {rickrolled_user}.")

@client.slash_command(name="savechat", description="Saves DM chat history with all guild members.")
async def savechat(interaction: nextcord.Interaction):
    for guild in client.guilds:
        for member in guild.members:
            if member.bot:
                continue

            try:
                dm_channel = member.dm_channel
                if not dm_channel:
                    dm_channel = await member.create_dm()

                dm_file = f"{member.id}_dms.txt"
                with open(dm_file, "w") as file:
                    async for message in dm_channel.history(limit=None, oldest_first=True):
                        if message.author.id == client.user.id:
                            file.write(f"User ID: {message.author.id}\nYou sent: {message.content}\n")
                        else:
                            file.write(f"User ID: {message.author.id}\nYou received: {message.content}\n")
            except nextcord.HTTPException as e:
                print(f"Error saving chat history with {member.name} ({member.id}): {e}")

    await interaction.response.send_message("Chat history saved (with potential exceptions).")

@client.slash_command(name="dm", description="Sends a DM to a user multiple times.")
async def dm(interaction: nextcord.Interaction, user: nextcord.User, message: str, times: int):
    dm_file = f"{user.id}_dms.txt"
    previous_messages = []

    try:
        with open(dm_file, "r") as file:
            previous_messages = file.readlines()
    except FileNotFoundError:
        pass

    for _ in range(times):
        try:
            await user.send(f"User ID: {interaction.user.id}\nYou were DM'd by {interaction.user.mention}: {message}")
            previous_messages.append(f"User ID: {interaction.user.id}\nYou sent: {message}\n")
        except nextcord.HTTPException:
            await interaction.response.send_message(f"Failed to send DM to {user.mention}.")

    with open(dm_file, "w") as file:
        file.writelines(previous_messages)

    await interaction.response.send_message(f"Successfully sent DM to {user.mention} {times} times.")

client.run(BOT_TOKEN)
