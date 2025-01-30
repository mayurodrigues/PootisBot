import os
import logging
import discord
import yt_dlp
import asyncio
from discord.ext import commands
from dotenv import load_dotenv
from erros import MENSAGENS_DE_ERRO  # Importa o dicionário de erros no arquivo separado

# Configura o logging de erros
logging.basicConfig(filename='bot.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv() # Carrega as variáveis de ambiente do .env

# Configura as permissões do bot
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

bot = commands.Bot(command_prefix='!', intents=INTENTS) # Configura o bot com o prefixo e as permissões

@bot.event # Aviso no terminal quando o bot estiver pronto
async def on_ready():
    comandos_desativados = [] # Inserir nome do comando entre aspas e sem prefixo

    for comando in comandos_desativados:
        comando = bot.get_command(comando)
        if comando:
            comando.enabled = False  # Desativa automaticamente se encontrar algum comando na lista

    # Lista os bots ativos mostrando em que servidores estão e seus nomes de usuário dentro deles
    for guild in bot.guilds:
        print(f'Iniciado como {bot.user} no servidor {guild.name}!')

@bot.event # Histórico de mensagens no servidor no terminal
async def on_message(message):
    print(f'Mensagem de {message.author}: {message.content}')

    # Garante que o bot não responda a si
    if message.author == bot.user:
        return

    # Processa os comandos a partir das mensagens
    await bot.process_commands(message)

@bot.event # Tratamento de erros
async def on_command_error(ctx, error):
    tipo_de_erro = type(error)
    if tipo_de_erro in MENSAGENS_DE_ERRO:
        message = MENSAGENS_DE_ERRO[tipo_de_erro]
        if callable(message):
            message = message(error)
        await ctx.reply(message.format(ctx=ctx))
    else:
        await ctx.send("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.")
        logging.error(f"Erro não tratado: {error}", exc_info=True)

# Comando: bot diz "Fala!" para quem executou o comando
@bot.command()
async def ola(ctx):
    await ctx.reply(f'Fala, {ctx.author.name}!')

# Comando: bot responde seu tempo de resposta para quem executou o comando
@bot.command()
async def ping(ctx):
    await ctx.reply(f'Pong! Aqui está seu ping: {round(bot.latency * 1000)}ms')

# Comando: bot responde uma brincadeira com quem digitou "!pong" ao invés de "!ping"
@bot.command()
async def pong(ctx):
    await ctx.reply(f'Escreveu errado, minha gatinha!')

# Comando: bot entra no canal de voz
@bot.command()
async def entrar(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
    else:
        await ctx.reply("Antes de executar o comando, você deve estar no canal de voz em que devo entrar!")

# Comando: bot sai do canal de voz
@bot.command()
async def sair(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.reply("Não estou em um canal de voz!")

bot.run(os.getenv('TOKEN')) # Inicia o bot com o token gravado no .env
