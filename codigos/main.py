import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

# Configura as permissões do bot
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

# Configura o bot com o prefixo e as permissões
bot = commands.Bot(command_prefix='!', intents=INTENTS)

# Evento: mensagem no terminal quando o bot estiver pronto
@bot.event
async def on_ready():
    # Lista os bots ativos mostrando em que servidores estão e seus nomes de usuário dentro deles
    for guild in bot.guilds:
        print(f'Iniciado como {bot.user} no servidor {guild.name}!')

# Histórico de mensagens no servidor no terminal
@bot.event
async def on_message(message):
    print(f'Mensagem de {message.author}: {message.content}')

    # Garante que o bot não responda a si
    if message.author == bot.user:
        return

    # Processa os comandos a partir das mensagens
    await bot.process_commands(message)

# Comando: bot diz "Fala!" para quem executou o comando
@bot.command()
async def ola(ctx):
    await ctx.send(f'Fala, {ctx.author.name}!')

# Comando: bot responde seu tempo de resposta para quem executou o comando
@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Aqui está seu ping: {round(bot.latency * 1000)}ms')

# Comando: bot responde uma brincadeira com quem digitou "!pong" ao invés de "!ping"
@bot.command()
async def pong(ctx):
    await ctx.send(f'Escreveu errado, minha gatinha!')

# Parte do comando futuro para mostrar a foto de perfil
#   embed = discord.Embed(title=f"Avatar de @{message.author.name}")

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Inicia o bot com o token gravado no .env
bot.run(os.getenv('TOKEN'))