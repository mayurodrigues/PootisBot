import os
import json
import disnake
import requests

def comandos_lastfm(bot):
    perfis_nuvem = 'perfis_lastfm.json'

    def carregar_perfis():
        if os.path.exists(perfis_nuvem):
            with open(perfis_nuvem, 'r') as arquivo:
                try:
                    return json.load(arquivo)
                except json.JSONDecodeError:
                    return {}
        return {}

    perfis_temp = carregar_perfis()

    def salvar_perfis(dados):
        with open(perfis_nuvem, 'w') as arquivo:
            json.dump(dados, arquivo, indent=4)

    @bot.command()
    async def fmcadastrar(ctx, usuario: str):
        if str(ctx.guild.id) not in perfis_temp:
            perfis_temp[str(ctx.guild.id)] = []

        if usuario in perfis_temp[str(ctx.guild.id)]:
            await ctx.reply('Esse perfil Last.fm já foi cadastrado!')
        else:
            try:
                info = {
                    'method': 'user.getInfo',
                    'user': usuario,
                    'format': 'json',
                    'api_key': f'{os.getenv("API_LASTFM")}'
                }
                saida_info = requests.get('http://ws.audioscrobbler.com/2.0/', params=info).json()
                teste = saida_info['user']
            except KeyError:
                await ctx.reply('Não encontrei nenhum perfil Last.fm com esse nome de usuário!')
            else:
                perfis_temp[str(ctx.guild.id)].append(usuario)
                salvar_perfis(perfis_temp)
                await ctx.reply('Usuário Last.fm cadastrado com sucesso!')

    @bot.command()
    async def fmlistar(ctx):
        embed = disnake.Embed(title=f'Usuários Cadastrados', color=0xBA0000)
        if str(ctx.guild.id) in perfis_temp and perfis_temp[str(ctx.guild.id)]:
            descricao = '\n'.join(perfis_temp[str(ctx.guild.id)])
            embed.description = descricao
            await ctx.send(embed=embed)
        else:
            await ctx.reply('Não há usuários Last.fm cadastrados nesse servidor')

    @bot.command()
    async def fmlimpar(ctx):
        if str(ctx.guild.id) in perfis_temp and perfis_temp[str(ctx.guild.id)]:
            perfis_temp[str(ctx.guild.id)] = []
            salvar_perfis(perfis_temp)
            await ctx.reply('A lista de usuários Last.fm cadastrados agora está vazia!')
        else:
            await ctx.reply('Não há usuários Last.fm cadastrados nesse servidor')

    @bot.command()
    async def fmremover(ctx, usuario):
        if str(ctx.guild.id) in perfis_temp and perfis_temp[str(ctx.guild.id)]:
            if usuario in perfis_temp[str(ctx.guild.id)]:
                perfis_temp[str(ctx.guild.id)].remove(usuario)
                await ctx.reply('O usuário Last.fm foi removido da lista do servidor!')
            else:
                await ctx.reply('Não encontrei esse usuário Last.fm na lista do servidor!')
        else:
            await ctx.reply('Não há usuários Last.fm cadastrados nesse servidor')

    @bot.command()
    async def fmperfil(ctx, usuario: str):
        info = {
            'method': 'user.getInfo',
            'user': usuario,
            'format': 'json',
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_info = requests.get('http://ws.audioscrobbler.com/2.0/', params=info).json()

        embed = disnake.Embed(title = f'Usuário {saida_info['user']['name']}', color = 0xBA0000)
        embed.description = (f'**Nome de Exibição:** {saida_info['user']['realname']}\n'
                             f'**Número de Scrobbles:** {saida_info['user']['playcount']}\n'
                             f'**Artistas Escutados:** {saida_info['user']['artist_count']}\n'
                             f'**Álbuns Escutados:** {saida_info['user']['album_count']}\n'
                             f'**Músicas Escutadas:** {saida_info['user']['track_count']}\n'
                             f'[Link para o perfil]({saida_info['user']['url']})')

        for image in saida_info['user']['image']:
            if image['size'] == 'extralarge':
                foto = image['#text']
                embed.set_thumbnail(url=f'{foto}')
                break

        recentes = {
            'method': 'user.getRecentTracks',
            'user': usuario,
            'format': 'json',
            'limit': 5,
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_recentes = requests.get('http://ws.audioscrobbler.com/2.0/', params = recentes).json()

        faixas = saida_recentes.get('recenttracks', {}).get('track', [])
        if faixas:
            dados = []
            for faixas in faixas:
                if faixas.get('@attr', {}).get('nowplaying') == 'true':
                    continue
                nome = faixas.get('name')
                artista = faixas.get('artist', {}).get('#text')
                dados.append(f'{artista} - {nome} ')

            embed.add_field(
                name = 'Atividade Recente',
                value = '\n'.join(dados),
                inline = False
            )
        else: pass

        await ctx.reply(embed = embed)

    @bot.command()
    async def fmtop(ctx, periodo: str, usuario: str):
        info = {
            'method': 'user.getInfo',
            'user': usuario,
            'format': 'json',
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_info = requests.get('http://ws.audioscrobbler.com/2.0/', params = info).json()
        embed = disnake.Embed(title = f'Usuário {saida_info['user']['name']}', color = 0xBA0000)

        for image in saida_info['user']['image']:
            if image['size'] == 'extralarge':
                foto = image['#text']
                embed.set_thumbnail(url = f'{foto}')
                break

        periodos = {
            'geral': 'overall',
            'semanal': '7days',
            'mensal': '1month',
            'trimestral': '3month',
            'semestral': '6month',
            'anual': '12moth'
        }

        artistas = {
            'method': 'user.getTopArtists',
            'user': usuario,
            'format': 'json',
            'limit': 5,
            'period': periodos[periodo],
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_artistas = requests.get('http://ws.audioscrobbler.com/2.0/', params = artistas).json()

        autores = saida_artistas.get('topartists', {}).get('artist', [])
        if autores:
            dados = []
            for autor in autores:
                nome = autor.get('name')
                dados.append(f'{nome} ')

            embed.add_field(
                name = 'Artistas mais ouvidos',
                value = '\n'.join(dados),
                inline = False
            )
        else: pass

        albuns = {
            'method': 'user.getTopAlbums',
            'user': usuario,
            'format': 'json',
            'limit': 5,
            'period': periodos[periodo],
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_albuns = requests.get('http://ws.audioscrobbler.com/2.0/', params = albuns).json()

        discos = saida_albuns.get('topalbums', {}).get('album', [])
        if discos:
            dados = []
            for disco in discos:
                nome = disco.get('name')
                artista = disco.get('artist', {}).get('name')
                dados.append(f'{artista} - {nome} ')

            embed.add_field(
                name = 'Álbuns mais tocados',
                value = '\n'.join(dados),
                inline = False
            )
        else: pass

        musicas = {
            'method': 'user.getTopTracks',
            'user': usuario,
            'format': 'json',
            'limit': 5,
            'period': periodos[periodo],
            'api_key': f'{os.getenv('API_LASTFM')}'
        }
        saida_recentes = requests.get('http://ws.audioscrobbler.com/2.0/', params = musicas).json()
        sons = saida_recentes.get('toptracks', {}).get('track', [])

        if sons:
            dados = []
            for som in sons:
                nome = som.get('name')
                artista = som.get('artist', {}).get('name')
                dados.append(f'{artista} - {nome} ')

            embed.add_field(
                name = 'Músicas mais escutadas',
                value ='\n'.join(dados),
                inline = False
            )

        await ctx.reply(embed = embed)

    @bot.command()
    async def fmplays(ctx, tipo: str, usuario: str):
        match tipo:
            case 'album':
                musicas = {
                    'method': 'user.getTopTracks',
                    'user': usuario,
                    'format': 'json',
                    'api_key': f'{os.getenv('API_LASTFM')}'
                }
                saida_recentes = requests.get('http://ws.audioscrobbler.com/2.0/', params=musicas).json()
                sons = saida_recentes.get('toptracks', {}).get('track', [])