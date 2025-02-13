from sympy import sympify
from re import fullmatch

def comandos_calcular(bot):
    substituicoes = {
        '×': '*',
        '÷': '/',
        ',': '.',
    }

    @bot.command()
    async def calcular(ctx, *args):
        operacao = ' '.join(args)
        for errado, certo in substituicoes.items():
            operacao = operacao.replace(errado, certo)

        if fullmatch(r'[0-9.+\-*/()\[\]{}% ]+', operacao.lower()):
            resultado = sympify(operacao)
            if resultado.is_Integer:
                await ctx.reply(f'Resultado: {int(resultado)}')
            elif resultado.is_rational:
                await ctx.reply(f'Resultado: {float(resultado)}')
            else:
                await ctx.reply(f'Resultado com decimal: {resultado.evalf()}\n'
                                f'Resultado com radical: {resultado}')
        elif operacao.lower() == 'o amor de mayu pela rosa':
            await ctx.reply('É imensurável…')
        else:
            await ctx.reply('Essa não é uma operação válida!')

