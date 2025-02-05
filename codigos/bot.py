import disnake
import logging
from disnake.ext import commands
from erros import MENSAGENS_DE_ERRO
from simples import comandos_simples
from musica import comandos_musica
from pesquisa import comandos_pesquisa
from calcular import comandos_calcular

# Configura o logging de erros
logging.basicConfig(filename='bot.log', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Configura as permissões do bot
INTENTS = disnake.Intents.default()
INTENTS.messages = True
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

# Cria uma instância do bot
bot = commands.Bot(command_prefix='!', intents=INTENTS)

# Evento: mensagem no terminal quando o bot inicia
@bot.event
async def on_ready():
    comandos_desativados = []  # Inserir nome do comando entre aspas e sem prefixo
    for comando in comandos_desativados:
        comando = bot.get_command(comando)
        if comando:
            comando.enabled = False  # Desativa automaticamente se encontrar algum comando na lista

    # Lista os bots ativos mostrando em que servidores estão e seus nomes de usuário dentro deles
    for guild in bot.guilds:
        print(f'Iniciado como {bot.user} no servidor {guild.name}!')

# Evento: exibe mensagens de chat no terminal
@bot.event
async def on_message(message):
    print(f'Mensagem de {message.author}: {message.content}')
    # Garante que o bot não responda a si
    if message.author == bot.user:
        return
    # Processa os comandos a partir das mensagens
    await bot.process_commands(message)

# Tratamento de erros
@bot.event
async def on_command_error(ctx, error):
    tipo_de_erro = type(error)
    if tipo_de_erro in MENSAGENS_DE_ERRO:
        mensagem = MENSAGENS_DE_ERRO[tipo_de_erro]
        if callable(mensagem):
            mensagem = mensagem(error)
        await ctx.reply(mensagem.format(ctx=ctx))
    else:
        await ctx.reply('Ocorreu um erro inesperado! Por favor, tente novamente.')
        print(error)
        logging.error(f'{error}', exc_info=True)

# Configura os comandos
comandos_simples(bot)
comandos_calcular(bot)
comandos_musica(bot)
comandos_pesquisa(bot)