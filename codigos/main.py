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

filas = {}

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
        await ctx.reply("Ocorreu um erro inesperado. Por favor, tente novamente mais tarde.")
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
        if ctx.guild.id in filas: # Verifica se havia uma fila para o servidor
            filas[ctx.guild.id].clear() # Se houver, limpa a fila ao sair
    else:
        await ctx.reply("Não estou em um canal de voz!")

@bot.command()
async def tocar(ctx, url):
    # Entra no canal de voz caso o bot não esteja em um
    if not ctx.voice_client:
        await entrar(ctx)

    # Cria uma fila para o servidor caso ainda não exista
    if ctx.guild.id not in filas:
        filas[ctx.guild.id] = []

    # Define as opções da biblioteca yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        loop = asyncio.get_event_loop()  # Permite que o bot funcione para outros comandos enquanto reproduz algo

        # Armazena as informações do vídeo na variável info sem baixá-lo
        info = await loop.run_in_executor(None, lambda: ydl.extract_info(url, download=False))

        if 'url' not in info:
            await ctx.reply("Erro ao obter o link! O vídeo pode estar privado ou indisponível.")
            return

        filas[ctx.guild.id].append({"url": info['url'], "title": info['title']}) # Adiciona o video à fila do servidor com título e utl

        # Verifica se há mais de um item na fila antes de enviar a mensagem de adicionado
        if ctx.voice_client.is_playing():
            await ctx.reply(f"Adicionado à fila: {info['title']}")
        else:
            await comecar(ctx)

# Função para começar a reprodução (não é um comando)
async def comecar(ctx):
    musica = filas[ctx.guild.id].pop(0)
    ffmpeg_options = {'options': '-vn'} # Remove o vídeo e extrai apenas o áudio

    # Converte o áudio para opus e cria um player (objeto) para tocá-lo no canal de audio
    source = discord.FFmpegOpusAudio(musica['url'], **ffmpeg_options)
    # Cria um player e toca o áudio no canal de voz
    ctx.voice_client.play(source, after=lambda e: asyncio.run_coroutine_threadsafe(comecar(ctx), bot.loop))
    await ctx.reply(f"Tocando agora: {musica['title']}")

@bot.command()
async def pausa(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing(): # Verifica se o usuário está num canal de voz e se algo está sendo reproduzido
        ctx.voice_client.pause() # Pausa a reprodução
        await ctx.reply('Reprodução pausada!')
    elif ctx.voice_client and ctx.voice_client.is_paused(): # Verifica se o usuário está num canal de voz e se há uma reprodução pausada
            ctx.voice_client.resume()
            await ctx.reply('Reprodução retomada!') # Retoma a reprodução
    else:
        await ctx.reply('Não há nada para pausar!')

# Comando: limpar a fila de reprodução
# @bot.command()
# async def limpar(ctx):
#     if ctx.guild.id in filas:
#         filas[ctx.guild.id].clear()
#         await ctx.reply("✅ Fila limpa!")
#     else:
#         await ctx.reply("❌ Não há fila para limpar!")

bot.run(os.getenv('TOKEN')) # Inicia o bot com o token gravado no .env
