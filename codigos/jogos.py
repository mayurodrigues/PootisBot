import disnake
from random import choice, randint

def comandos_jogos(bot):
    # Comando: lança um dado padrão ou de lados especificados
    @bot.command()
    async def dado(ctx, escolha: str = None):
        dado = escolha or 'd6'
        resultados = {1: 'Um (1)!', 2: 'Dois (2)!', 3: 'Três (3)!', 4: 'Quatro (4)!', 5: 'Cinco (5)!',
                      6: 'Seis (6)!', 7: 'Sete (7)!', 8: 'Oito (8)!', 9: 'Nove (9)!', 10: 'Dez (10)!',
                      11: 'Onze (11)!', 12: 'Doze (12)!', 13: 'Treze (13)!', 14: 'Catorze (14)!', 15: 'Quinze (15)!',
                      16: 'Dezesseis (16)!', 17: 'Dezessete (17)!', 18: 'Dezoito (18)!', 19: 'Dezenove (19)!', 20: 'Vinte (20)!'}

        gif = disnake.File('material/rolagem_dados.gif', filename='rolagem_dados.gif')
        embed = disnake.Embed(title='O resultado é…', color=0xffffff)
        embed.set_thumbnail(file=gif)

        match dado:
            case 'd4':
                numero = randint(1, 4)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case 'd6':
                numero = randint(1, 6)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case 'd8':
                numero = randint(1, 8)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case 'd10':
                numero = randint(1, 10)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case 'd12':
                numero = randint(1, 12)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case 'd20':
                numero = randint(1, 20)
                embed.description = resultados[numero]
                await ctx.reply(embed=embed)
            case _:
                await ctx.reply('Os dados disponíveis são: d4, d6, d8, d10, d12 e d20!')

    # Comando: lança uma moeda para um cara ou coroa
    @bot.command()
    async def moeda(ctx):
        resultado = choice(['cara', 'coroa'])
        embed = disnake.Embed(title='O resultado é…', color=0xFFD700)
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