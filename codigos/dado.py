from random import randint
import disnake

def comandos_dado(bot):
    # Comando: lança um dado de seis lados
    @bot.command()
    async def dado(ctx):
        resultado = randint(1, 6)
        match resultado:
            case 1:
                dado = disnake.File('material/dado1.png', filename='dado1.png')
                await ctx.reply(file=dado)
            case 2:
                dado = disnake.File('material/dado2.png', filename='dado2.png')
                await ctx.reply(file=dado)
            case 3:
                dado = disnake.File('material/dado3.png', filename='dado3.png')
                await ctx.reply(file=dado)
            case 4:
                dado = disnake.File('material/dado4.png', filename='dado4.png')
                await ctx.reply(file=dado)
            case 5:
                dado = disnake.File('material/dado5.png', filename='dado5.png')
                await ctx.reply(file=dado)
            case 6:
                dado = disnake.File('material/dado6.png', filename='dado6.png')
                await ctx.reply(file=dado)