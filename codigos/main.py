import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

permissoes = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents = permissoes)

@bot.event
async def on_ready():
    print("Estou online!")

load_dotenv()
bot.run(os.getenv('TOKEN'))