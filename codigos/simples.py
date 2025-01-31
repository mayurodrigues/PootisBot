import discord

def comandos_simples(bot):
    @bot.command
    async def ola(ctx):
        """
        Responde com uma saudação ao usuário.
        """
        await ctx.reply(f'Fala, {ctx.author.name}!')

    @bot.command
    async def ping(ctx):
        """
        Responde com o ping do bot.
        """
        await ctx.reply(f'Pong! Aqui está seu ping: {round(bot.latency * 1000)}ms!')

    @bot.command
    async def pong(ctx):
        """
        Responde com uma brincadeira ao comando "!pong".
        """
        await ctx.reply('Escreveu errado, minha gatinha!')

    @bot.command
    async def avatar(ctx, membro: discord.Member = None):
        """
        Responde com a foto de perfil do autor ou um usuário específico.
        """
        membro = membro or ctx.author
        embed = discord.Embed(
            title=f'Avatar de {membro.name}',
            # color=discord.Color.blue()
        )
        embed.set_image(url=membro.avatar.url)
        await ctx.reply(embed=embed)