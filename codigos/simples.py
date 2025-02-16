import disnake
from disnake.ext import commands
from datetime import datetime

def comandos_simples(bot):
    # Comando: exibe as informações dos comandos do bot
    @bot.command()
    async def ajuda(ctx):
        embed = disnake.Embed(color=0xCD7F32)
        embed.add_field(name='Comandos Gerais:',
                        value=('**!ping:** responde o ping (latência) entre o usuário e o bot.\n'
                               '**!avatar:** exibe a foto de perfil do autor da mensagem ou de um usuário marcado.\n'
                               '**!calcular:** envia o resultado de uma operação matemática especificada.\n'
                               '**!pesquisar:** envia os três primeiros resultados de uma pesquisa no Google pelo termo especificado, com títulos, links e pequenas descrições.\n'
                               '**!dado:** lança um dado padrão ou um especificado (d4, d6, d8, d10, d12 e d20).\n'
                               '**!moeda:** responde um resultado aleatório de “Cara ou Coroa”.'), inline=False)
        embed.add_field(name='Comandos de Música:',
                        value=('**!entrar:** entra no canal de voz do autor da mensagem.\n'
                               '**!sair:** sai do canal de voz em que está.\n'
                               '**!tocar:** reproduz o áudio do URL fornecido ou o adiciona à fila de reprodução.\n'
                               '**!pausar:** pausa ou retoma a reprodução atual.\n'
                               '**!pular:** alterna o áudio em reprodução pelo próximo da fila.\n'
                               '**!agora:** responde as informações do áudio em reprodução.\n'
                               '**!fila:** exibe os áudios presentes na lista de reprodução.\n'
                               '**!remover:** remove o áudio presente na posição específicada da fila.\n'
                               '**!limpar:** remove todos os áudios presentes na fila de reprodução.'), inline=False)
        embed.set_footer(text='Pootis Bot v1.0 • Desenvolvido por Lisa e Mayu',icon_file=disnake.File('material/bot.jpg', filename='bot.jpg'))
        await ctx.reply(embed=embed)

    # Comando: bot responde com uma saudação ao usuário
    @bot.command()
    async def ola(ctx):
        await ctx.reply(f'Fala, {ctx.author.name}!')

    # Comando: bot responde com o ping do usuário
    @bot.command()
    async def ping(ctx):
        await ctx.reply(f'Pong! Aqui está seu ping: {round(bot.latency * 1000)}ms.')

    # Comando: bot responde com uma brincadeira
    @bot.command()
    async def pong(ctx):
        await ctx.send(f'{ctx.author.mention} tentou se pingar!')

    # Comando: bot exibe a foto de perfil do autor da mensagem ou de um usuário específico
    @bot.command()
    async def avatar(ctx, membro: disnake.Member = None):
        membro = membro or ctx.author
        embed = disnake.Embed(title=f'Avatar de {membro.name}')
        embed.set_image(url=membro.avatar.url)
        await ctx.reply(embed=embed)

    # Comando: bot exibe informações a respeito do autor da mensagem ou de um usuário específico
    @bot.command()
    async def userinfo(ctx, membro: disnake.Member = None):
        membro = membro or ctx.author
        status = {'online': 'Online', 'idle': 'Ausente', 'dnd': 'Não perturbar', 'offline': 'Offline'}

        criacao = f'{membro.created_at}'
        meses = {1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
                 5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
                 9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"}
        data_criacao = datetime.strptime(criacao[:10], "%Y-%m-%d")
        dia_criacao = data_criacao.day
        mes_criacao = meses[data_criacao.month]
        ano_criacao = data_criacao.year

        embed = disnake.Embed(title = f'Informações de {membro.display_name}')
        embed.set_thumbnail(url=membro.avatar.url)

        if isinstance(membro, disnake.User):
            embed.description = (f'**Usuário:** {membro.name}\n'
                                 f'**Conta criada em:** {dia_criacao} de {mes_criacao} de {ano_criacao}\n')
            await ctx.reply(embed=embed)
        else:
            entrada = f'{membro.joined_at}'
            data_entrada = datetime.strptime(entrada[:10], "%Y-%m-%d")
            dia_entrada = data_entrada.day
            mes_entrada = meses[data_entrada.month]
            ano_entrada = data_entrada.year

            embed.description = (f'**Usuário:** {membro.name}\n'
                                 f'**Status:** {status[f'{membro.status}']}\n'
                                 f'**Conta criada em:** {dia_criacao} de {mes_criacao} de {ano_criacao}\n'
                                 f'**Entrou no servidor em:** {dia_entrada} de {mes_entrada} de {ano_entrada}')
            await ctx.send(embed=embed)

    # @bot.command()
    # @commands.guild_only()
    # async def serverinfo(ctx):
