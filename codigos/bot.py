import discord
import logging
from discord.ext import commands
from erros import MENSAGENS_DE_ERRO  # Importa o dicionário de erros no arquivo separado
from comandos_simples import comandos_simples  # Importa comandos simples
from musica import comandos_musica  # Importa comandos de música

# Configura o logging de erros
logging.basicConfig(filename='bot.log', level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura as permissões do bot
INTENTS = discord.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

# Cria uma instância do bot
bot = commands.Bot(command_prefix='!', intents=INTENTS)

@bot.event
async def on_ready():
    """
    Evento disparado quando o bot está pronto e conectado ao Discord.
    """
    comandos_desativados = []  # Inserir nome do comando entre aspas e sem prefixo

    for comando in comandos_desativados:
        comando = bot.get_command(comando)
        if comando:
            comando.enabled = False  # Desativa automaticamente se encontrar algum comando na lista

    # Lista os bots ativos mostrando em que servidores estão e seus nomes de usuário dentro deles
    for guild in bot.guilds:
        print(f'Iniciado como {bot.user} no servidor {guild.name}!')

@bot.event
async def on_message(message):
    """
    Evento disparado quando uma mensagem é enviada no servidor.
    """
    print(f'Mensagem de {message.author}: {message.content}')

    # Garante que o bot não responda a si
    if message.author == bot.user:
        return

    # Processa os comandos a partir das mensagens
    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    """
    Evento disparado quando ocorre um erro em um comando.
    """
    tipo_de_erro = type(error)
    if tipo_de_erro in MENSAGENS_DE_ERRO:
        message = MENSAGENS_DE_ERRO[tipo_de_erro]
        if callable(message):
            message = message(error)
        await ctx.reply(message.format(ctx=ctx))
    else:
        await ctx.reply('Ocorreu um erro inesperado. Por favor, tente novamente mais tarde!')
        logging.error(f'Erro não tratado: {error}', exc_info=True)

# Configura comandos simples e de música
comandos_simples(bot)
comandos_musica(bot)