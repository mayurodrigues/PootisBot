import disnake

def comandos_simples(bot):
    # Comando: exibe as informações dos comandos do bot
    @bot.command()
    async def ajuda(ctx):
        embed = disnake.Embed(title='Lista de comandos')
        embed.description = ('**!ping:** responde o ping (latência) entre o usuário e o bot.\n'
                             '**!avatar:** exibe a foto de perfil do autor da mensagem, quando não há marcações, ou de um usuário marcado.\n'
                             '**!calcular:** envia o resultado de uma operação matemática especificada\n'
                             '**!dado:** lança um dado de seis lados.\n'
                             '**!moeda:** responde um resultado aleatório de “Cara ou Coroa”.\n'
                             '**!entrar:** entra no canal de voz do autor da mensagem (o bot não pode reproduzir áudios em múltiplos canais).\n'
                             '**!sair:** sai do canal de voz em que está.\n'
                             '**!tocar:** reproduz o áudio do URL fornecido (apenas vídeos do YouTube) ou o adiciona à fila de reprodução existente.\n'
                             '**!pausar:** pausa ou retoma a reprodução atual.\n'
                             '**!pular:** alterna o áudio em reprodução pelo próximo da fila.\n'
                             '**!agora:** responde as informações do áudio em reprodução.\n'
                             '**!fila:** exibe os áudios presentes na lista de reprodução.\n'
                             '**!remover:** remove o áudio presente na posição específicada da fila.\n'
                             '**!limpar:** remove todos os áudios presentes na fila de reprodução.\n'
                             '**!pesquisa:** envia os três primeiros resultados de uma pesquisa no Google pelo termo especificado, com títulos, links e pequenas descrições.' )
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