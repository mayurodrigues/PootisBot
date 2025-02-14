import disnake
from random import choice, randint

def comandos_jogos(bot):
    # Comando: lança um dado de seis lados
    @bot.command()
    async def dado(ctx):
        resultado = randint(1, 6)
        embed = disnake.Embed(title='O resultado é…', color=0xffffff)
        gif = disnake.File('material/rolagem_dados.gif', filename='rolagem_dados.gif')
        match resultado:
            case 1:
                embed.set_thumbnail(file=gif)
                embed.description = 'Um (1)!'
                await ctx.reply(embed=embed)
            case 2:
                embed.set_thumbnail(file=gif)
                embed.description = 'Dois (2)!'
                await ctx.reply(embed=embed)
            case 3:
                embed.set_thumbnail(file=gif)
                embed.description = 'Três (3)!'
                await ctx.reply(embed=embed)
            case 4:
                embed.set_thumbnail(file=gif)
                embed.description = 'Quatro (4)!'
                await ctx.reply(embed=embed)
            case 5:
                embed.set_thumbnail(file=gif)
                embed.description = 'Cinco (5)!'
                await ctx.reply(embed=embed)
            case 6:
                embed.set_thumbnail(file=gif)
                embed.description = 'Seis (6)!'
                await ctx.reply(embed=embed)

    # Comando: lança uma moeda para um cara ou coroa
    @bot.command()
    async def moeda(ctx):
        resultado = choice(['cara', 'coroa'])
        embed = disnake.Embed(title='O resultado é…', color=0x8B8000)
        gif = disnake.File('material/giro_moeda.gif', filename='giro_moeda.gif')
        match resultado:
            case 'cara':
                embed.set_thumbnail(file=gif)
                embed.description = 'Cara!'
                await ctx.reply(embed=embed)
            case 'coroa':
                embed.set_thumbnail(file=gif)
                embed.description = 'Coroa!'
                await ctx.reply(embed=embed)