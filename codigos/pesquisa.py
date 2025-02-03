import os
import disnake
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_GOOGLE = os.getenv('API_GOOGLE')
ID_SIMPLES = os.getenv('ID_SIMPLES')
SIMPLES = build('customsearch', 'v1', developerKey=API_GOOGLE) # Constroi um mecanismo de busca

def comandos_pesquisa(bot):
    @bot.command()
    async def pesquisar(ctx, *args):
        termo = ' '.join(args) # Define tudo escrito após o comando como parte do termo a ser pesquisado
        LOGO = disnake.File('material/google_logo.png', filename='google_logo.png') # Variável de arquivo para a logo na pasta (material)
        embed = disnake.Embed(title=f'Resultados para “{termo}”', colour=0x4285F4)
        embed.set_footer(text=f'Google Search', icon_file=LOGO) # Configura o rodapé

        pesquisa = SIMPLES.cse().list(q=termo, cx=ID_SIMPLES, num=3, hl='pt-BR', gl='br', searchType='image').execute()

        if 'items' in pesquisa and pesquisa['items']: # Pega a imagem presente no primeiro resultado, se houver
            imagem = pesquisa['items'][0].get('link')
        else: imagem = None

        pesquisa = SIMPLES.cse().list(q=termo, cx=ID_SIMPLES, num=3, hl='pt-BR', gl='br').execute()
        for numero, resultado in enumerate(pesquisa.get('items', [])):
            titulo = resultado.get('title', 'Sem título')
            link = resultado.get('link', 'Sem link')
            descricao = resultado.get('snippet', 'Sem descrição')

            embed.add_field(name=f'**{numero + 1}. {titulo}**', value=f'{descricao}\n[Acessar link]({link})',inline=False)

        if imagem: embed.set_thumbnail(url=imagem) # Adiciona a imagem extraída do primeiro resultado como thumb
        await ctx.send(embed=embed, file=LOGO)
