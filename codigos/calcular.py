from sympy import sympify
from re import fullmatch

def comandos_calcular(bot):
    substituicoes = {
        '×': '*',
        '÷': '/',
        ',': '.',
    }

    # Comando: bot resolve um cálculo
    @bot.command()
    async def calcular(ctx, *args):
        operacao = ' '.join(args)
        # Substituir símbolos inválidos pelos corretos
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
        else:
            await ctx.reply('Essa não é uma operação válida!')

