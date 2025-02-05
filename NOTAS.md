### Propriedades do ctx (contexto)
* **ctx.author:** retorna o usuário que executou o comando;
* * _id, name, mention, display_name, avatar, created_at, joined_at, roles…_
* **ctx.channel:** retorna o canal onde o comando foi executado;
* * _id, name, guild…_
* **ctx.guild:** retorna o servidor onde o comando foi executado;
* * _id, name, owner, member_count, roles, channels, icon, created_at…_
* **ctx.message**: retorna a mensagem que acionou o comando;
* * _id, content, author, channel, guild, created_at, attachments, reactions…_
* **ctx.command:** retorna o comando acionado na mensagem;
* * _name, description, help, checks…_
* Use **ctx.bot** para propriedades do bot.
* * _user, guilds, latency, commands owner_id…_

### Métodos do ctx (contexto)
* **ctx.voice_client:** retorna o cliente de voz do servidor;
* **ctx.send():** envia uma mensagem no canal onde o comando foi executado;
* **ctx.reply():** envia a mensagem no formato de resposta do discord;
* **ctx.trigger_typing():** exibe o status “digitando” no canal para o bot;
* **ctx.invoke():** aciona outro comando dentro do contexto atual;
* **ctx.purge():** apaga mensagens no canal atual;
* **ctx.voice_client.connect** e **disconnect**: controlam a entrada e saída do bot em canais de voz;
* **ctx.guild.fetch_member**: busca um membro do servidor pelo id.

### Decoradores do discord.py
* **@bot.event:** define funções automáticas;
* **@bot.command:** define funções ativados através do chat;
* Usar **@bot.command()** para decoradores de comando dentro de funções.