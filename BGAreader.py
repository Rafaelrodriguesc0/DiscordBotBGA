import discord
from discord.ext import commands, tasks
import asyncio
import requests
from bs4 import BeautifulSoup

# Bot token
TOKEN = 'YOUR_DISCORD_BOT_TOKEN'

# Define intents
intents = discord.Intents.default()
intents.messages = True

# Create bot instance with specified intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Function to scrape the webpage and get the active player
def get_active_player():
    url = 'https://pt.boardgamearena.com/10/gaiaproject?table=492791046'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        active_player_tag = soup.find('div', {'id': 'active_player'})
        if active_player_tag:
            active_player = active_player_tag.text.strip()
            return active_player
    return None

# Task to periodically check for active player and send message
@tasks.loop(minutes=1)
async def check_active_player():
    channel_id = 1223625214709993585  # Replace with your channel ID
    previous_active_player = None
    active_player = get_active_player()
    if active_player and active_player != previous_active_player:
        # Send message to Discord channel
        channel = bot.get_channel(channel_id)
        if channel:
            await channel.send(f"It's {active_player}'s turn!")
        else:
            print("Channel not found.")
        previous_active_player = active_player

# Event: Bot is ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    check_active_player.start()

# Run the bot
bot.run(TOKEN)
