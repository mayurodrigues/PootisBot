import discord
import yt_dlp as youtube_dl
import asyncio
from discord.ext import commands

# Dicionário para armazenar as filas de reprodução de cada servidor
filas = {}

def comandos_musica(bot):
    @bot.command()
    async def tocar(ctx, url: str):
        """
        Adiciona uma música à fila e começa a reprodução.
        """
        async def comecar():
            if not filas[ctx.guild.id]:  # Verifica se a fila está vazia
                return

            musica = filas[ctx.guild.id].pop(0)  # Remove a primeira música da fila

            # Configurações do ffmpeg para reprodução de áudio
            ffmpeg_options = {
                'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
                'options': '-vn -filter:a "volume=0.5"'
            }

            # Prepara o áudio
            source = discord.FFmpegOpusAudio(musica['url'], **ffmpeg_options)

            # Função chamada após a reprodução terminar
            def proxima(e):
                if e:
                    print(f'Erro ao tocar a música: {e}')
                if filas[ctx.guild.id]:  # Se ainda houver músicas na fila, toca a próxima
                    asyncio.run_coroutine_threadsafe(comecar(), bot.loop)

            # Toca o áudio no canal de voz
            ctx.voice_client.play(source, after=proxima)
            await ctx.reply(f'Tocando agora: {musica["title"]}!')

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

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                # Executa o yt-dlp em uma thread separada para não bloquear o loop de eventos
                info = await asyncio.to_thread(ydl.extract_info, url, download=False)

                if 'url' not in info:
                    await ctx.reply('Erro ao obter o link! O vídeo pode estar privado ou indisponível!')
                    return

                musica = {'url': info['url'], 'title': info['title']}
                filas[ctx.guild.id].append(musica)  # Adiciona a música na fila

                # Se não houver música tocando, inicia a reprodução
                if not ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                    await comecar()
                else:
                    await ctx.reply(f'Adicionado à fila: {musica["title"]}!')

            except youtube_dl.utils.DownloadError as e:
                await ctx.reply(f'Erro ao processar o link: {str(e)}!')
            except Exception as e:
                await ctx.reply('Erro ao processar o link! O vídeo pode estar indisponível ou não ser compatível!')
                print(f'Erro ao extrair informações do vídeo: {e}')

    @bot.command()
    async def pausa(ctx):
        """
        Pausa ou retoma a reprodução da música.
        """
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()  # Pausa a reprodução
            await ctx.reply('Reprodução pausada!')
        elif ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()  # Retoma a reprodução
            await ctx.reply('Reprodução retomada!')
        else:
            await ctx.reply('Não há nada para pausar!')

    @bot.command
    async def pular(ctx):
        """
        Pula para a próxima música na fila.
        """
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Para a música atual, chamando o after para tocar a próxima
            await ctx.reply('Música pulada!')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    @bot.command
    async def agora(ctx):
        """
        Mostra qual música está tocando no momento.
        """
        if ctx.voice_client and ctx.voice_client.is_playing():
            musica = filas[ctx.guild.id][0] if filas[ctx.guild.id] else None  # Verifica se há algo na fila
            if musica:
                embed = discord.Embed(
                    title='Tocando Agora:',
                    description=f'{musica["title"]}',
                    # color=discord.Color.blue()
                )
                await ctx.reply(embed=embed)
            else:
                await ctx.reply('Nenhuma música está sendo reproduzida no momento!')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    @bot.command()
    async def fila(ctx):
        """
        Exibe a fila de reprodução atual.
        """
        if ctx.guild.id in filas and filas[ctx.guild.id]:
            embed = discord.Embed(title='Fila de Reprodução:', color=discord.Color.blue())
            for i, musica in enumerate(filas[ctx.guild.id], start=1):
                embed.add_field(name=f'{i}. {musica["title"]}', value='\u200b', inline=False)
            await ctx.reply(embed=embed)
        else:
            await ctx.reply('A fila está vazia!')

    @bot.command()
    async def limpar(ctx):
        """
        Limpa a fila de reprodução.
        """
        if ctx.guild.id in filas:
            filas[ctx.guild.id].clear()
            await ctx.reply('Fila limpa!')
        else:
            await ctx.reply('Não há fila para limpar!')

    @bot.command()
    async def entrar(ctx):
        """
        Entra no canal de voz do usuário.
        """
        if ctx.author.voice:  # Verifica se o usuário está em um canal de voz
            canal = ctx.author.voice.channel
            if ctx.voice_client:
                await ctx.voice_client.move_to(canal)  # Move o bot para o canal do usuário
            else:
                await canal.connect()  # Conecta o bot ao canal de voz
            await ctx.reply(f'Entrei no canal de voz: {canal.name}!')
        else:
            await ctx.reply('Você precisa estar em um canal de voz para usar este comando!')

    @bot.command()
    async def sair(ctx):
        """
        Sai do canal de voz.
        """
        if ctx.voice_client:  # Verifica se o bot está conectado a um canal de voz
            await ctx.voice_client.disconnect()
            await ctx.reply('Saí do canal de voz!')
        else:
            await ctx.reply('Não estou em um canal de voz!')

    @bot.command()
    async def remover(ctx, posicao: int):
        """
        Remove uma música específica da fila.
        """
        if ctx.guild.id in filas and 1 <= posicao <= len(filas[ctx.guild.id]):
            musica_removida = filas[ctx.guild.id].pop(posicao - 1)
            await ctx.reply(f'Removida da fila: {musica_removida["title"]}!')
        else:
            await ctx.reply('Posição inválida ou fila vazia!')