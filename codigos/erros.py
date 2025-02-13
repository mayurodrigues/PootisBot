from disnake.ext import commands

MENSAGENS_DE_ERRO = {
    commands.CommandNotFound: 'Comando incorreto ou inexistente! Use "!ajuda" para uma lista dos comandos ou verifique sua mensagem.',
    commands.BadArgument: 'Um argumento inválido foi utilizado na execução desse comando! Use "!ajuda" para entender a sintaxe ou verifique sua mensagem.',
    commands.MissingRequiredArgument: 'Faltam argumentos necessários para a execução desse comando! Use "!ajuda" para entender a sintaxe ou verifique sua mensagem.',
    commands.TooManyArguments: 'Você forneceu argumentos demais! Use "!ajuda" para entender a sintaxe ou verifique sua mensagem.',
    commands.BadColourArgument: 'Essa não é uma cor válida!',
    commands.MissingPermissions: 'Você não tem permissão para executar esse comando!',
    commands.PrivateMessageOnly: 'Esse comando deve ser utilizado apenas em mensagens privadas!',
    commands.NoPrivateMessage: 'Esse comando não pode ser utilizado em mensagens privadas!',
    commands.DisabledCommand: 'Esse comando está desativado no momento!',
    commands.CommandOnCooldown: lambda error: f'Esse comando está em tempo de espera! Tente novamente em {round(error.retry_after)} segundos.',
    commands.MemberNotFound: 'Não há nenhum membro com esse nome aqui!',
    commands.UserNotFound: 'Não existe nenhum usuário com o nome e ID fornecido!'
}