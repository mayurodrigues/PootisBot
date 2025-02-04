import os
import disnake
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

API_GOOGLE = os.getenv('API_GOOGLE')
ID_SIMPLES = os.getenv('ID_SIMPLES')
SIMPLES = build('customsearch', 'v1', developerKey=API_GOOGLE)  # Constrói um mecanismo de busca

def comandos_pesquisa(bot):
    @bot.command()
    async def pesquisar(ctx, *args):
        termo = ' '.join(args)  # Define tudo escrito após o comando como parte do termo a ser pesquisado
        LOGO = disnake.File('material/google_logo.png', filename='google_logo.png')  # Variável de arquivo para a logo na pasta (material)
        embed = disnake.Embed(title=f'Resultados para “{termo}”', colour=0x4285F4)
        embed.set_footer(text='Google Search', icon_url='attachment://google_logo.png')  # Configura o rodapé

        # Faz a pesquisa normal (sem searchType='image') para obter sites
        pesquisa = SIMPLES.cse().list(q=termo, cx=ID_SIMPLES, num=3, hl='pt-BR', gl='br', key=API_GOOGLE).execute()

        # Verifica se há resultados e pega o link do primeiro site
        if 'items' in pesquisa and pesquisa['items']:
            # Faz uma segunda pesquisa para encontrar uma imagem relacionada ao primeiro site
            pesquisa_imagem = SIMPLES.cse().list(q=termo, cx=ID_SIMPLES, num=1, hl='pt-BR', gl='br', searchType='image', key=API_GOOGLE).execute()
            if 'items' in pesquisa_imagem and pesquisa_imagem['items']:
                imagem = pesquisa_imagem['items'][0].get('link')  # URL da imagem
            else: imagem = None
        else:
            await ctx.send(f'Não encontrei nenhum resultado para "{termo}"!')
            return

        # Adiciona os resultados da pesquisa ao embed
        for numero, resultado in enumerate(pesquisa.get('items', [])):
            titulo = resultado.get('title', 'Sem título')
            link = resultado.get('link', 'Sem link')
            descricao = resultado.get('snippet', 'Sem descrição')

            embed.add_field(
                name=f'**{numero + 1}. {titulo}**',
                value=f'{descricao}\n[Acessar link]({link})',
                inline=False
            )

        # Adiciona a imagem como thumbnail, se encontrada
        if imagem: embed.set_thumbnail(url=imagem)
        await ctx.send(embed=embed)