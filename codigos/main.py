import os
import discord
from discord.ext import commands
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


# Na variável "permissões" são colocadas as permissões, que precisam ser ativadas como acontece abaixo
permissoes = discord.Intents.default()
permissoes.messages = True
permissoes.message_content = True

# Criando um client
client = MyClient(intents=permissoes)

#
# @client.command(aliases=['p', 'q'])
# async def ping(ctx, arg=None):
#     if arg == "pong":
#         await ctx.send('Nice job, you just ponged yourself')
#     else:
#         await ctx.send(f'Pong! Here is your ping: {round(client.latency * 1000)}ms')

load_dotenv()
client.run(os.getenv('TOKEN'))