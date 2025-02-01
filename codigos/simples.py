import discord

def comandos_simples(bot):
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
        await ctx.reply(f'Escreveu errado, {ctx.user.name}!')

    # Comando: bot exibe a foto de perfil do autor da mensagem ou de um usuário específico
    @bot.command()
    async def avatar(ctx, membro: discord.Member = None):
        membro = membro or ctx.author
        embed = discord.Embed(title=f'Avatar de {membro.name}')
        embed.set_image(url=membro.avatar.url)
        await ctx.reply(embed=embed)