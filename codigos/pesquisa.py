import os
import disnake
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API = os.getenv('GOOGLE_API')
ID_BASICO = os.getenv('BASICO')

def comandos_pesquisa(bot):
    @bot.command()
    async def pesquisar(ctx, termo: str):
        logo = disnake.File('material/google_logo.png', filename='google_logo.png')

        embed = disnake.Embed(title=f'Resultados para: {termo}', colour=0x4285F4)
        embed.set_thumbnail(file=logo)
        embed.set_author(name="Google Search", icon_file=logo)
        embed.timestamp = ctx.message.created_at

        basico = build('customsearch', 'v1', developerKey=API)
        pesquisa = basico.cse().list(q=termo, cx=ID_BASICO, num=3, hl='pt-BR', gl='br').execute()

        for numero, resultado in enumerate(pesquisa.get('items', [])):
            titulo = resultado.get('title', 'Sem título')
            link = resultado.get('link', 'Sem link')
            descricao = resultado.get('snippet', 'Sem descrição')
            embed.add_field(name=f'{titulo}', value=f'{descricao}\n[Link]({link})', inline=False)

        await ctx.send(embed=embed)