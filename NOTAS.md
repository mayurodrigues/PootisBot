### Propriedades e métodos do ctx (contexto)
- ctx.author: o usuário que executou o comando
- ctx.channel: o canal onde o comando foi executado
- ctx.guild: o servidor onde o comando foi executado
- ctx.message: a mensagem que contém o comando
- ctx.send(): envia uma mensagem no canal onde o comando foi executado
- ctx.reply(): envia a mensagem no formato de resposta do discord

### Decoradores do discord.py
- @bot.event: define funções automáticas
- @bot.command: define funções ativados através do chat
- *Usar **@bot.command()** para decoradores de comando dentro de funções*