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

load_dotenv()  # Carrega as variáveis de ambiente do .env

# Configura as permissões do bot
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

bot = commands.Bot(command_prefix='!', intents=INTENTS)  # Configura o bot com o prefixo e as permissões

filas = {}  # Dicionário para armazenar as filas de reprodução de cada servidor

@bot.event  # Aviso no terminal quando o bot estiver pronto
async def on_ready():
    comandos_desativados = []  # Inserir nome do comando entre aspas e sem prefixo

    for comando in comandos_desativados:
        comando = bot.get_command(comando)
        if comando:
            comando.enabled = False  # Desativa automaticamente se encontrar algum comando na lista

    # Lista os bots ativos mostrando em que servidores estão e seus nomes de usuário dentro deles
    for guild in bot.guilds:
        print(f'Iniciado como {bot.user} no servidor {guild.name}!')

@bot.event  # Histórico de mensagens no servidor no terminal
async def on_message(message):
    print(f'Mensagem de {message.author}: {message.content}')

    # Garante que o bot não responda a si
    if message.author == bot.user:
        return

    # Processa os comandos a partir das mensagens
    await bot.process_commands(message)

@bot.event  # Tratamento de erros
async def on_command_error(ctx, error):
    tipo_de_erro = type(error)
    if tipo_de_erro in MENSAGENS_DE_ERRO:
        message = MENSAGENS_DE_ERRO[tipo_de_erro]
        if callable(message):
            message = message(error)
        await ctx.reply(message.format(ctx=ctx))
    else:
        await ctx.reply('Ocorreu um erro inesperado. Por favor, tente novamente mais tarde!')
        logging.error(f'Erro não tratado: {error}', exc_info=True)

# Comando: bot diz "Fala!" para quem executou o comando
@bot.command()
async def ola(ctx):
    await ctx.reply(f'Fala, {ctx.author.name}!')

# Comando: bot responde seu tempo de resposta para quem executou o comando
@bot.command()
async def ping(ctx):
    await ctx.reply(f'Pong! Aqui está seu ping: {round(bot.latency * 1000)}ms!')

# Comando: bot responde uma brincadeira com quem digitou "!pong" ao invés de "!ping"
@bot.command()
async def pong(ctx):
    await ctx.reply('Escreveu errado, minha gatinha!')

@bot.command()
async def tocar(ctx, url: str):
    # Função para começar a reprodução da próxima música na fila
    async def comecar():
        if not filas[ctx.guild.id]:  # Verifica se há músicas na fila
            return

        reproducao = filas[ctx.guild.id].pop(0)  # Remove a primeira música da fila

        # Configurações do ffmpeg para reprodução de áudio
        ffmpeg_options = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn -filter:a "volume=0.5"'
        }

        source = discord.FFmpegOpusAudio(reproducao['url'], **ffmpeg_options)

        # Função chamada após a reprodução terminar
        def after_playing(e):
            if e:
                print(f'Erro ao tocar a música: {e}')
            if filas[ctx.guild.id]:  # Se ainda houver músicas na fila, toca a próxima
                asyncio.run_coroutine_threadsafe(comecar(), bot.loop)

        ctx.voice_client.play(source, after=after_playing)
        await ctx.send(f'Tocando agora: {reproducao["title"]}!')

    # Verifica se o usuário está em um canal de voz
    if not ctx.author.voice:
        await ctx.reply('Você precisa estar em um canal de voz para tocar músicas!')
        return

    # Entra no canal de voz caso o bot não esteja em um
    if not ctx.voice_client:
        canal = ctx.author.voice.channel
        await canal.connect()

    # Cria uma fila para o servidor caso ainda não exista
    if ctx.guild.id not in filas:
        filas[ctx.guild.id] = []

    # Define as opções do yt-dlp para extração de informações do vídeo
    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            # Executa o yt-dlp em uma thread separada para não bloquear o loop de eventos
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)

            if 'url' not in info:
                await ctx.reply('Erro ao obter o link! O vídeo pode estar privado ou indisponível!')
                return

            musica = {'url': info['url'], 'title': info['title']}
            filas[ctx.guild.id].append(musica)  # Adiciona a música na fila

            # Exibe a fila para depuração
            print(f'Fila atual ({ctx.guild.id}):', filas[ctx.guild.id])

            # Se não houver música tocando, inicia a reprodução
            if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await comecar()
            else:
                await ctx.reply(f'Adicionado à fila: {musica["title"]}!')

        except yt_dlp.utils.DownloadError as e:
            await ctx.reply(f'Erro ao processar o link: {str(e)}!')
        except Exception as e:
            await ctx.reply('Erro ao processar o link! O vídeo pode estar indisponível ou não ser compatível!')
            print(f'Erro ao extrair informações do vídeo: {e}')
    print(filas)

# Comando: pausar ou retomar a reprodução
@bot.command()
async def pausa(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()  # Pausa a reprodução
        await ctx.reply('Reprodução pausada!')
    elif ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()  # Retoma a reprodução
        await ctx.reply('Reprodução retomada!')
    else:
        await ctx.reply('Não há nada para pausar!')

# Comando: pular para o próximo item da fila de reprodução
@bot.command()
async def pular(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()  # Para a música atual, chamando o after para tocar a próxima
        await ctx.reply('Música pulada!')
    else:
        await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

# Comando: informa o que está sendo reproduzido
@bot.command()
async def agora(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        musica = filas[ctx.guild.id][0] if filas[ctx.guild.id] else None  # Verifica se há algo na fila
        if musica:
            embed = discord.Embed(
                title='Tocando Agora:',
                description=f'{musica["title"]}',
                color=discord.Color.blue()
            )
            await ctx.reply(embed=embed)
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')
    else:
        await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

# Comando: exibir a fila atual
@bot.command()
async def fila(ctx):
    if ctx.guild.id in filas and filas[ctx.guild.id]:
        embed = discord.Embed(title='Fila de Reprodução:', color=discord.Color.blue())
        for i, musica in enumerate(filas[ctx.guild.id], start=1):
            embed.add_field(name=f'{i}. {musica["title"]}', value='\u200b', inline=False)
        await ctx.reply(embed=embed)
    else:
        await ctx.reply('A fila está vazia!')

# Comando: limpar a fila de reprodução
@bot.command()
async def limpar(ctx):
    if ctx.guild.id in filas:
        filas[ctx.guild.id].clear()
        await ctx.reply('Fila limpa!')
    else:
        await ctx.reply('Não há fila para limpar!')

# Comando: entrar no canal de voz
@bot.command()
async def entrar(ctx):
    if ctx.author.voice:  # Verifica se o usuário está em um canal de voz
        canal = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(canal)  # Move o bot para o canal do usuário
        else:
            await canal.connect()  # Conecta o bot ao canal de voz
        await ctx.reply(f'Entrei no canal de voz: {canal.name}!')
    else:
        await ctx.reply('Você precisa estar em um canal de voz para usar este comando!')

# Comando: sair do canal de voz
@bot.command()
async def sair(ctx):
    if ctx.voice_client:  # Verifica se o bot está conectado a um canal de voz
        await ctx.voice_client.disconnect()  # Desconecta do canal de voz
        await ctx.reply('Saí do canal de voz!')
    else:
        await ctx.reply('Não estou em um canal de voz!')

# Comando: remover uma música específica da fila
@bot.command()
async def remover(ctx, posicao: int):
    if ctx.guild.id in filas and 1 <= posicao <= len(filas[ctx.guild.id]):
        musica_removida = filas[ctx.guild.id].pop(posicao - 1)
        await ctx.reply(f'Removida da fila: {musica_removida["title"]}!')
    else:
        await ctx.reply('Posição inválida ou fila vazia!')

bot.run(os.getenv('TOKEN'))  # Inicia o bot com o token gravado no .env