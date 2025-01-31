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

async def texto_imagem(image, top_text=None, bottom_text=None):
    try:
        font_path = "C:/Users/Gabriel/Desktop/PootisBot/PootisBot/fontes/TR Impact.ttf"
        font_size = int(image.height * 0.10)
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("Fonte Impact não encontrada. Usando fonte padrão.")

    draw = ImageDraw.Draw(image)
    text_color = (255, 255, 255)
    outline_color = (0,0,0)
    outline_width = 3

    if top_text:
        text_bbox = draw.textbbox((0, 0), top_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = ((image.width - text_width) // 2, 10)
        draw.text(
            position, 
            top_text, 
            font=font, 
            fill=text_color, 
            stroke_width=outline_width, 
            stroke_fill=outline_color
        )


    if bottom_text:
        text_bbox = draw.textbbox((0, 0), bottom_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        position = (
            (image.width - text_width) // 2, 
            image.height - text_height - 20
            ) 
        draw.text(
            position, 
            bottom_text, 
            font=font, 
            fill=text_color,
            stroke_width=outline_width,
            stroke_fill=outline_color,
        )

    return image

async def processa_imagem(attachment, top_text=None, bottom_text=None):
    image_bytes = await attachment.read()
    image = Image.open(io.BytesIO(image_bytes))

    if getattr(image, "is_animated", False):
        frames = []
        durations = []
        for frame in ImageSequence.Iterator(image):
            frame = frame.convert("RGBA")
            frame = await texto_imagem(frame, top_text, bottom_text)
            frames.append(frame)
            durations.append(frame.info.get("duration", 100))

        gif_binary = io.BytesIO()
        frames[0].save(
            gif_binary,
            format="GIF",
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=durations
        )
        gif_binary.seek(0)
        return gif_binary, "gif"
    else:
        image = await texto_imagem(image.convert("RGBA"), top_text, bottom_text)
        image_binary = io.BytesIO()
        image.save(image_binary, format="PNG")
        image_binary.seek(0)
        return image_binary, "png"

@bot.command()
async def meme(ctx, *, text: str):
    if not ctx.message.attachments:
        await ctx.send("Anexe um arquivo!")
        return

    attachment = ctx.message.attachments[0]
    if not attachment.filename.lower().endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp')):
        await ctx.send("Por favor, anexe um arquivo válido!")
        return


    top_text = None
    bottom_text = None
    if ',' in text:
        parts = text.split(',')
        if len(parts) == 2:
            top_text = parts[0].replace("tt", "").strip()
            bottom_text = parts[1].replace("bt", "").strip()
    else:
        top_text = text.replace("tt", "").strip()

    output, format = await processa_imagem(attachment, top_text, bottom_text)

    try:
        if format == "gif":
            await ctx.send(file=discord.File(fp=output, filename='image_with_text.gif'))
        else:
            await ctx.send(file=discord.File(fp=output, filename='image_with_text.png'))
    finally:
        output.close()




# Carrega as variáveis de ambiente do .env
load_dotenv()

# Inicia o bot com o token gravado no .env
bot.run(os.getenv('TOKEN'))