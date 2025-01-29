import os
import discord
from dotenv import load_dotenv

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Iniciado como {self.user}!')

    async def on_message(self, message):
         # Ignorar mensagens do próprio bot
        if message.author == self.user:
            return

        print(f'Mensagem de {message.author}: {message.content}')
        if message.content == '!ola':
            await message.channel.send(f'Fala, {message.author.name}!')

        elif message.content == '!ping':
            await message.channel.send(f'Pong! Aqui está seu ping: {round(client.latency * 1000)}ms.')

        elif message.content == '!pong':
            await message.channel.send('Escreveu errado, minha gatinha!')

        elif message.content == '!avatar':
            embed = discord.Embed(title=f"Avatar de @{message.author.name}")

# Na variável "permissões" são colocadas as permissões, que precisam ser ativadas como acontece abaixo
permissoes = discord.Intents.default()
permissoes.messages = True
permissoes.message_content = True

# Criando um client
client = MyClient(intents=permissoes)

load_dotenv()
client.run(os.getenv('TOKEN'))