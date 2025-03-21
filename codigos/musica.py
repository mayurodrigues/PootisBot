import disnake
from disnake.ext import commands
import yt_dlp as youtube_dl
import asyncio

filas = {}  # Dicionário para armazenar as filas de reprodução por servidor
atual = {}  # Armazena o que está sendo tocado no momento em cada servidor

def comandos_musica(bot):
    # Comando: entra no canal de voz do usuário
    @bot.command()
    @commands.guild_only()
    async def entrar(ctx):
        if ctx.author.voice:
            if ctx.voice_client:
                await ctx.voice_client.move_to(ctx.author.voice.channel)  # Move para o canal do usuário, se já estiver em outro
            else:
                await ctx.author.voice.channel.connect()  # Conecta ao canal de voz do usuário
            await ctx.reply(f'Entrei no canal de voz “{ctx.author.voice.channel.name}”!')
        else:
            await ctx.reply('Você precisa estar em um canal de voz para usar este comando!')

    # Comando: sai do canal de voz
    @bot.command()
    @commands.guild_only()
    async def sair(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.reply('Saí do canal de voz!')
        else:
            await ctx.reply('Não estou em um canal de voz!')

    # Comando: toca o áudio do url fornecido ou o adiciona à lista
    @bot.command()
    @commands.guild_only()
    async def tocar(ctx, url: str):
        # Define as opções do yt-dlp para extração de informações do vídeo
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True,
            'default_search': False,
            'source_address': '0.0.0.0'
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # Verifica se o usuário está em um canal de voz
            if not ctx.author.voice:
                await ctx.reply('Você precisa estar em um canal de voz!')
                return
            # Entra no canal de voz caso o bot não esteja em um
            if not ctx.voice_client:
                await ctx.author.voice.channel.connect()
            # Cria uma fila para o servidor caso ainda não exista
            if ctx.guild.id not in filas:
                filas[ctx.guild.id] = []

            # Função chamada ao iniciar uma reprodução
            async def comecar():
                # Extrai o primeiro vídeo da fila e define como atual
                atual[ctx.guild.id] = filas[ctx.guild.id].pop(0)

                # Configurações do ffmpeg para reprodução de áudio
                ffmpeg_options = {'options': '-vn -filter:a "volume=0.5" -latency 50 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

                # Converte o áudio para opus com as configurações estabelecidas e armazena o URL numa variável
                player = disnake.FFmpegOpusAudio(atual[ctx.guild.id]['url'], **ffmpeg_options)

                # Função que mantém o player funcionando e tocando o próximo áudio da fila
                async def proxima(ctx):
                    if ctx.guild.id in filas and filas[ctx.guild.id]:
                        await comecar()
                    else:
                        await ctx.reply('Não há mais nada para tocar!')
                        await ctx.voice_client.disconnect()

                # Toca o áudio no canal de voz e anuncia
                ctx.voice_client.play(player, after=lambda: asyncio.run_coroutine_threadsafe(proxima(ctx), bot.loop))
                await ctx.reply(f'**Tocando agora:** {atual[ctx.guild.id]['title']}!')

            # Executa o yt-dlp em uma thread separada para não bloquear o loop de eventos e extrai as informações do vídeo
            info = await asyncio.to_thread(ydl.extract_info, url, download=False)

            # Verifica o acesso ao link do vídeo
            if 'url' not in info:
                await ctx.reply('Não foi possível acessar esse URL! Verifique sua mensagem ou a disponibilidade do link.')
                return
            else:
                # Adiciona o url e o título do video na fila
                nova = {'url': info['url'], 'title': info['title']}
                filas[ctx.guild.id].append(nova)

            if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
                await ctx.reply(f'**Adicionado à fila:** {nova['title']}!')
            else:
                await comecar()

    # Comando: pausa ou retoma a reprodução
    @bot.command()
    @commands.guild_only()
    async def pausar(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()  # Pausa a reprodução
            await ctx.reply('Reprodução pausada!')
        elif ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()  # Retoma a reprodução
            await ctx.reply('Reprodução retomada!')
        else:
            await ctx.reply('Não há nada para pausar!')

    # Comando: pula para a próxima música
    @bot.command()
    @commands.guild_only()
    async def pular(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing() or ctx.voice_client.is_paused:
            ctx.voice_client.stop()  # Interrompe a reprodução atual, acionando a função "proxima"
            await ctx.reply('Música pulada!')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    # Comando: mostra o que está tocando no momento
    @bot.command()
    @commands.guild_only()
    async def agora(ctx):
        if ctx.guild.id in atual:
            await ctx.reply(f'**Tocando Agora:** {atual[ctx.guild.id]["title"]}')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    # Comando: exibe a fila de reprodução
    @bot.command()
    @commands.guild_only()
    async def fila(ctx):
        if ctx.guild.id in filas and filas[ctx.guild.id]:
            embed = disnake.Embed(title='Fila de Reprodução:')
            for numero, musica in enumerate(filas[ctx.guild.id], start=1):
                embed.add_field(name=f'{numero}. {musica["title"]}', value='\u200b', inline=False)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply('A fila está vazia!')

    # Remove um vídeo da fila
    @bot.command()
    @commands.guild_only()
    async def remover(ctx, posicao: int):
        if ctx.guild.id in filas and 1 <= posicao <= len(filas[ctx.guild.id]):
            musica_removida = filas[ctx.guild.id].pop(posicao - 1)
            await ctx.reply(f'Removida da fila: {musica_removida["title"]}!')
        else:
            await ctx.reply('Posição inválida ou fila vazia!')

    # Comando: limpa a fila de reprodução
    @bot.command()
    @commands.guild_only()
    async def limpar(ctx):
        if ctx.guild.id in filas:
            filas[ctx.guild.id].clear()
            await ctx.reply('Fila limpa!')
        else:
            await ctx.reply('Não há fila para limpar!')

    # Evento: apaga a fila se o bot for desconectado
    @bot.event
    @commands.guild_only()
    async def on_voice_state_update(member, after):
        if member == bot.user and after.channel is None:
            if member.guild.id in filas:
                del filas[member.guild.id]
            if member.guild.id in atual:
                del atual[member.guild.id]