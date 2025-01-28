import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

CHANNEL_ID = 1333909539820666934

permissoes = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents = permissoes)

@bot.command()
async def ola(ctx:commands.Context):
    usuario = ctx.author
    await ctx.reply(f"Falaaaa assombrados!{usuario.name}")

@bot.event
async def on_ready():
    print("Estou online!")
    channel = bot.get_channel(CHANNEL_ID)
    await channel.send("Fala gatinhas! Estou na área!")

load_dotenv()
bot.run(os.getenv('TOKEN'))