import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageSequence
import io

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

async def texto_imagem(image, text, position):
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    text_color = (255, 255, 255)
    draw.text(position, text, font=font, fill=text_color)
    return image


async def processa_imagem(attachment, text, position):
    image_bytes = await attachment.read()
    image = Image.open(io.BytesIO(image_bytes))

    if getattr(image, "is_animated", False):
        frames = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.convert("RGBA")
            frame = await texto_imagem(frame, text, position)
            frames.append(frame)

            gif_binary = io.BytesIO()
            frames[0].save(
                gif_binary,
                format="GIF",
                save_all=True,
                append_images=frames[1:],
                loop=0,  # Loop infinito
                duration=image.info.get("duration", 100)
            )

            gif_binary.seek(0)
            return gif_binary, "gif"

    else:
        image = await texto_imagem(image.convert("RGBA"), text, position)
        image_binary = io.BytesIO()
        image.save(image_binary, format="PNG")
        image_binary.seek(0)
        return image_binary, "png"

# Comando: bot responde com a imagem e texto que o usuário enviou
@bot.command()
async def tt(ctx, *, text: str):
    if not ctx.message.attachments:
        await ctx.send("Anexe um arquivo!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
        await ctx.send("Por favor, anexe um arquivo válido!")
        return

    text_position = (10, 10)
    output, format = await processa_imagem(attachment, text, text_position)

    try:
        if format == "gif":
            await ctx.send(file=discord.File(fp=output, filename='image_with_top_text.gif'))
        else:
            await ctx.send(file=discord.File(fp=output, filename='image_with_top_text.png'))
    finally:
        output.close()

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Inicia o bot com o token gravado no .env
bot.run(os.getenv('TOKEN'))