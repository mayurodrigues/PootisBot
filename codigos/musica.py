import discord
import yt_dlp as youtube_dl
import asyncio

filas = {}  # Dicionário para armazenar as filas de reprodução por servidor
atual = {}  # Armazena o que está sendo tocado no momento em cada servidor

def comandos_musica(bot):
    # Comando: entra no canal de voz do usuário
    @bot.command()
    async def entrar(ctx):
        if ctx.author.voice:
            if ctx.voice_client:
                await ctx.voice_client.move_to(
                    ctx.author.voice.channel)  # Caso o bot esteja num canal de voz diferente, move para o do usuário
            else:
                await ctx.author.voice.channel.connect()  # Conecta o bot ao canal de voz do usuário
            await ctx.reply(f'Entrei no canal de voz "{ctx.author.voice.channel.name}"!')
        else:
            await ctx.reply('Você precisa estar em um canal de voz para usar este comando!')

    # Comando: sai do canal de voz
    @bot.command()
    async def sair(ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.reply('Saí do canal de voz!')
        else:
            await ctx.reply('Não estou em um canal de voz!')

    # Comando: toca o áudio do url fornecido ou o adiciona à lista
    @bot.command()
    async def tocar(ctx, url: str):
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
            # Avisa quando a fila estiver vazia
            if not filas[ctx.guild.id]:
                await ctx.send('A fila acabou!')
                return

            atual[ctx.guild.id] = filas[ctx.guild.id].pop(0)  # Extrai o primeiro vídeo da fila e define como atual

            # Configurações do ffmpeg para reprodução de áudio
            ffmpeg_options = {'options': '-vn -filter:a "volume=0.5" -latency 50 -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}

            # Converte o áudio para opus com as configurações estabelecidas e o armazena numa variável
            source = discord.FFmpegOpusAudio(atual[ctx.guild.id]['url'], **ffmpeg_options)

            # Função chamada após a reprodução terminar
            def proxima(error = None):
                if error:
                    print(f"Erro durante a reprodução: {error}")

                if filas[ctx.guild.id]:  # Se ainda houver músicas na fila, toca a próxima
                    asyncio.run_coroutine_threadsafe(comecar(), bot.loop)

            # Toca o áudio no canal de voz
            ctx.voice_client.play(source, after=proxima)
            await ctx.reply(f'Tocando agora: {atual[ctx.guild.id]["title"]}!')

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

            # Se não houver música tocando, inicia a reprodução. Se houver, adiciona o video à fila
            if ctx.voice_client.is_playing() and not ctx.voice_client.is_paused():
                await ctx.reply(f'Adicionado à fila: {nova["title"]}!')
            else:
                await comecar()

    # Comando: pausa ou retoma a reprodução
    @bot.command()
    async def pausa(ctx):
        # Pausa a reprodução se o usuário estiver num canal de voz onde algo está sendo reproduzido
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()  # Pausa a reprodução
            await ctx.reply('Reprodução pausada!')
       # Retoma a reprodução se o usuário estiver num canal de voz onde há uma reprodução pausada
        elif ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()  # Retoma a reprodução
            await ctx.reply('Reprodução retomada!')
        else:
            await ctx.reply('Não há nada para pausar!')

    # Comando: pula para a próxima música
    @bot.command()
    async def pular(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()  # Se algo estiver tocando, a música atual, chamando a função "proxima"
            await ctx.reply('Música pulada!')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    # Comando: mostra o que está tocando no momento
    @bot.command()
    async def agora(ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            # Se houver algo tocando, guarda as informações na variável abaixo, se não houver, deixa vazia
            musica = filas[ctx.guild.id][0] if filas[ctx.guild.id] else None
            # Se houver informações de video na variável, exibe no chat
            if musica:
                embed = discord.Embed(title='Tocando Agora:', description=f'{musica["title"]}',
                )
                await ctx.reply(embed=embed)
            else:
                await ctx.reply('Nenhuma música está sendo reproduzida no momento!')
        else:
            await ctx.reply('Nenhuma música está sendo reproduzida no momento!')

    # Comando: exibe a fila de reprodução
    @bot.command()
    async def fila(ctx):
        # Verifica se há uma fila nesse servidor e se a fila não está vazia, para criar um embed com as informações dela
        if ctx.guild.id in filas and filas[ctx.guild.id]:
            embed = discord.Embed(title='Fila de Reprodução:')
            # Adiciona os vídeos presentes na fila no embed com um índice numérico
            for numero, musica in enumerate(filas[ctx.guild.id], start=1):
                embed.add_field(name=f'{numero}. {musica["title"]}', value='\u200b', inline=False)
            await ctx.reply(embed=embed) # Manda o embed da lista no chat
        else:
            await ctx.reply('A fila está vazia!')

    # Remove um video da fila
    @bot.command()
    async def remover(ctx, posicao: int):
        if ctx.guild.id in filas and 1 <= posicao <= len(filas[ctx.guild.id]):
            musica_removida = filas[ctx.guild.id].pop(posicao - 1)
            await ctx.reply(f'Removida da fila: {musica_removida["title"]}!')
        else:
            await ctx.reply('Posição inválida ou fila vazia!')

    # Comando: limpa a fila de reprodução
    @bot.command()
    async def limpar(ctx):
        if ctx.guild.id in filas:
            filas[ctx.guild.id].clear()
            await ctx.reply('Fila limpa!')
        else:
            await ctx.reply('Não há fila para limpar!')


